# *- coding:utf8 *-
import json
import os

from flask import request, jsonify

from Fansti.config.Inforcode import mch_key, mch_id, APP_ID, APP_SECRET_KEY, base_dir, ip
from Fansti.libs.weixin import WeixinPay, WeixinLogin, WeixinError


class CPay(object):
    def __init__(self):
        self._check_file()

    def pay_service(self):
        """付款, 需要openid和num"""
        args = request.json or {}
        num = args.get('num', 1)
        ip = request.headers.get('X-Real-Ip', request.remote_addr)
        try:
            total_fee = int(num)
            openid = args.get('openid')
            if not openid:
                raise TypeError
        except TypeError as e:
            return jsonify({
                "status": 404,
                "message": '参数有误'
            })
        out_trade_no = self.pay.nonce_str
        try:
            raw = self.pay.jsapi(trade_type="JSAPI", openid=openid, body='body',
                                 out_trade_no=out_trade_no,
                                 total_fee=int(total_fee), attach='attac', spbill_create_ip=ip)
            res = dict(raw)
            res['paySign'] = res.get('sign')
        except WeixinError as e:
            return jsonify({
                "status": 404,
                "message": e.args,
                'ip': ip
            })
        res = dict(raw)
        res['paySign'] = res.get('sign')
        return res

    def pay_notify(self):
        """支付回调"""
        print('pay_notify')
        data = self.pay.to_dict(request.data)
        if not self.pay.check(data):
            return self.pay.reply(u"签名验证失败", False)
        paytime = data.get('time_end')
        history = {paytime: data.get('total_fee')}
        self._append_history(history)
        return self.pay.reply("OK", True)

    def pay_hitory(self):
        """获取历史"""
        print('pay_history')
        return jsonify(
            {
                "status": 200,
                "data": self._pay_history
            }
        )

    @property
    def _pay_history(self):
        """获取历史"""
        pay_history = os.path.join(base_dir, 'pay_history.txt')
        with open(pay_history, 'r') as rf:
            content = rf.read() or '[]'
            history = json.loads(content)
        return history

    def _append_history(self, data):
        """插入一条记录"""
        history = self._pay_history
        history.append(data)
        pay_history = os.path.join(base_dir, 'pay_history.txt')
        with open(pay_history, 'w') as wf:
            content = json.dumps(history)
            wf.write(content)

    def _check_file(self):
        pay_history = os.path.join(base_dir, 'pay_history.txt')
        is_exists = os.path.isfile(pay_history)
        if not is_exists:
            with open(pay_history, 'w') as wf:
                wf.write('[]')

    @property
    def pay(self):
        notify_url = ip + 'fansti/pay/pay_notify'
        # APP_ID = 'wx284751ea4c889568'
        # mch_key = 'HangZhouZhenLangHangZhouZhenLang'
        # mch_id = '1504082901'
        return WeixinPay(APP_ID, mch_id, mch_key, notify_url)


if __name__ == '__main__':
    cpay = CPay()
