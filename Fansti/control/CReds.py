# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import datetime, calendar, json

from Fansti.config.Inforcode import mch_key, mch_id, APP_ID, APP_SECRET_KEY
from Fansti.libs.weixin import WeixinPay, WeixinLogin, WeixinError
from flask import request, jsonify
from Fansti.config.response import SYSTEM_ERROR, NETWORK_ERROR
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list
from Fansti.common.import_status import import_status

class CReds():
    def __init__(self):
        from Fansti.services.SReds import SReds
        self.sred = SReds()
        from Fansti.services.SUsers import SUsers
        self.suser = SUsers()

    def get_all_red(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_params = ["login_name"]
        if judge_keys(true_params, args.keys()) != 200:
            return judge_keys(true_params, args.keys())
        all_red = get_model_return_list(self.sred.get_my_red_status(args["login_name"]))
        make_log("all_red", all_red)
        response = import_status("SUCCESS_GET_RED", "OK")
        response["data"] = {}
        response["data"]["red_list"] = []
        for red in all_red:
            red_id = red["red_id"]
            red_abo = get_model_return_dict(self.sred.get_red_by_id(red_id))
            make_log("red_abo", red_abo)
            if not red_abo:
                return SYSTEM_ERROR
            red["name"] = red_abo["name"]
            red["price"] = red_abo["price"]
            #red["createtime"] = red["createtime"].strftime("%Y-%m-%d")
            response["data"]["red_list"].append(red_abo)
        response["data"]["red_num"] = len(get_model_return_list(self.sred.get_my_red_rereceive(args["login_name"])))
        response["data"]["red_list"] = all_red
        my_red = get_model_return_list(self.sred.get_my_red_receive(args["login_name"]))
        response["data"]["my_red_num"] = len(my_red)
        all_price = 0
        for red in my_red:
            a_red = get_model_return_dict(self.sred.get_red_by_id(red["red_id"]))
            make_log("a_red", a_red)
            red["createtime"] = red["createtime"].strftime("%Y-%m-%d")
            if not a_red:
                return SYSTEM_ERROR
            red["name"] = a_red["name"]
            red["price"] = a_red["price"]
            all_price = all_price + float(a_red["price"])

        response["data"]["my_red_list"] = my_red
        response["data"]["my_red_coin"] = all_price
        response["data"]["month_red"] = []
        month = 1
        while month < 13:
            my_red_month = get_model_return_list(self.sred.get_my_red_by_time(
                datetime.datetime(datetime.datetime.now().year, month, 1, 0, 0, 0),
                datetime.datetime(datetime.datetime.now().year, month, calendar.monthrange(
                    datetime.datetime.now().year, month)[1], 23, 59, 59)
            ))
            month_red = {
                "month": month,
                "count": len(my_red_month)
            }
            response["data"]["month_red"].append(month_red)
            month = month + 1
        print(response)
        return response

    def receive_red(self):
        """红包提现"""
        data = request.json or {}
        make_log("args", data)
        red_id = data.get('red_id')
        response = import_status("SUCCESS_GET_INFO", "OK")
        # 判断用户是否有这个红包
        openid = data.get('openid')
        user = self.suser.get_user_by_openid(openid)
        if not user:
            return jsonify({
                "status": 404,
                "message": "非法用户"
            })
        login_name = user.login_name
        user_red = self.sred.get_userred_by_loginname_redid(login_name, red_id)
        if not user_red:
            return jsonify({
                "status": 404,
                "message": "红包状态错误"
            })
        red = self.sred.get_red_new_by_id(user_red.red_id)
        if not red:
            return jsonify({
                "status": 404,
                "message": "不存在的红包"
            })
        # 计算金额, 退款
        amount = int(red.price) * 100
        desc = '红包领取'
        partner_trade_no = user_red.id.replace('-', '')
        # data = self.wx_login.jscode2session(openid)
        try:
            raw = self.pay.pay_individual(
                openid=openid, amount=amount, partner_trade_no=partner_trade_no,
                spbill_create_ip=request.remote_addr, desc=desc
            )
        except WeixinError as e:
            return jsonify({
                "status": 404,
                "message": e.args
            })
        # 改状态
        user_red = self.sred.update_user_red_by_id(user_red.id, {
            'status': 2
        })
        response['data'] = raw
        return response

    def receive_red_query(self):
        """"""
        data = request.json or {}
        # red_id = data.get('red_id')
        id = data.get('id')
        # 判断用户是否有这个红包
        openid = data.get('openid')
        # user = self.suser.get_user_by_openid(openid)
        # if not user:
        #     return jsonify({
        #         "status": 404,
        #         "message": "非法用户"
        #     })
        # login_name = user.login_name
        # user_red = self.sred.get_userred_by_loginname_redid(login_name, red_id, status=2)
        user_red = self.sred.get_userred_by_id(id)
        if not user_red:
            return jsonify({
                "status": 404,
                "message": "红包状态错误"
            })
        response = import_status("SUCCESS_GET_INFO", "OK")
        partner_trade_no = user_red.id.replace('-', '')
        try:
            raw = self.pay.pay_individual_query(partner_trade_no=partner_trade_no)
        except WeixinError as e:
            return jsonify({
                "status": 404,
                "message": e.args
            })
        response['data'] = raw
        return response

    @property
    def pay(self):
        return WeixinPay(APP_ID, mch_id, mch_key, key='./apiclient_key.pem',
                         cert='./apiclient_cert.pem')

    @property
    def wx_login(self):
        return WeixinLogin(APP_ID, APP_SECRET_KEY)
