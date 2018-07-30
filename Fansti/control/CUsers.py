# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import json, uuid
from flask import request
from Fansti.config.response import SYSTEM_ERROR, NETWORK_ERROR
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.get_model_return_list import get_model_return_dict
from Fansti.common.import_status import import_status
from Fansti.common.TransformToList import add_model

class CUsers():
    def __init__(self):
        from Fansti.services.SUsers import SUsers
        self.susers = SUsers()

    def user_binding(self):
        data = json.loads(request.data)
        make_log("data", data)
        true_data = ["login_name", "login_password", "phone", "openid"]
        if judge_keys(true_data, data.keys()) != 200:
            return judge_keys(true_data, data.keys())
        name_password_phone = get_model_return_dict(self.susers.get_name_password_phone(data["login_name"]))
        make_log("name_password_phone", name_password_phone)
        if not name_password_phone:
            return import_status("ERROR_NONE_USER", "FANSTI_ERROR", "ERROR_NONE_USER")
        if data["login_password"] != name_password_phone["login_password"]:
            return import_status("ERROR_WRONG_PASSWORD", "FANSTI_ERROR", "ERROR_WRONG_PASSWORD")
        else:
            wechat_login = get_model_return_dict(self.susers.get_wechat_login(data["login_name"]))
            make_log("wechat_login", wechat_login)
            if not wechat_login:
                add_wechat_login = add_model("WECHAT_LOGIN",
                                         **{
                                             "id": str(uuid.uuid1()),
                                             "login_name": data["login_name"],
                                             "openid": data["openid"],
                                             "status": "1",
                                             "phone": data["phone"]
                                         })
                make_log("add_wechat_login", add_wechat_login)
                if not add_wechat_login:
                    return SYSTEM_ERROR
            else:
                update_wechat_login = self.susers.update_wechat_login(data["login_name"],
                                                                      {
                                                                          "openid": data["openid"],
                                                                          "phone": data["phone"],
                                                                          "status": "1"
                                                                      })
                make_log("update_wechat_login", update_wechat_login)
                if not update_wechat_login:
                    return SYSTEM_ERROR

        return import_status("SUCCESS_USER_BINDING", "OK")

    def get_binding(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_params = ["openid"]
        if judge_keys(true_params, args.keys()) != 200:
            return judge_keys(true_params, args.keys())
        get_status_by_openid = get_model_return_dict(self.susers.get_wechat_login_by_openid(args["openid"]))
        make_log("get_status_by_openid", get_status_by_openid)
        if not get_status_by_openid:
            return import_status("ERROR_NONE_BINDING", "FANSTI_ERROR", "ERROR_NONE_BINDING")
        else:
            return import_status("ERROR_HAVE_BINDING", "FANSTI_ERROR", "ERROR_HAVE_BINDING")

    def get_openid(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_params = ["code"]
        if judge_keys(true_params, args.keys()) != 200:
            return judge_keys(true_params, args.keys())
        from Fansti.config.Inforcode import APP_ID, APP_SECRET_KEY
        request_url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type={3}" \
            .format(APP_ID, APP_SECRET_KEY, args["code"], "authorization_code")
        strResult = None
        try:
            import urllib2
            req = urllib2.Request(request_url)
            response = urllib2.urlopen(req)
            strResult = response.read()
            response.close()
            make_log("strResult", strResult)
        except Exception as e:
            print e.message
            return NETWORK_ERROR
        jsonResult = json.loads(strResult)
        if "openid" not in strResult or "session_key" not in strResult:
            return jsonResult
        openid = jsonResult["openid"]
        response = import_status("SUCCESS_GET_OPENID", "OK")
        response["data"] = {}
        response["data"]["openid"] = openid
        return response


