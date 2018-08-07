# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import json, uuid
from flask import request
from Fansti.config.response import SYSTEM_ERROR, NETWORK_ERROR
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list
from Fansti.common.import_status import import_status
from Fansti.common.TransformToList import add_model
from HTMLParser import HTMLParser
class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

class CUsers():
    def __init__(self):
        from Fansti.services.SUsers import SUsers
        self.susers = SUsers()
        from Fansti.services.SReds import SReds
        self.sreds = SReds()

    def user_binding(self):
        data = json.loads(request.data)
        make_log("data", data)
        true_data = ["phone", "openid"]
        null_data = ["login_name", "login_password", "name", "usex", "city", "province"]
        if judge_keys(true_data, data.keys(), null_data) != 200:
            return judge_keys(true_data, data.keys(), null_data)
        if self.get_wechat_phone(data["phone"]) != 200:
            return self.get_wechat_phone(data["phone"])
        if "login_name" in data and "login_password" in data:
            # TODO 判断是否存在当前月红包，存在的话
            name_password_phone = get_model_return_dict(self.susers.get_name_password_phone(data["login_name"]))
            make_log("name_password_phone", name_password_phone)
            if not name_password_phone:
                return import_status("ERROR_NONE_USER", "FANSTI_ERROR", "ERROR_NONE_USER")
            if data["login_password"] != name_password_phone["login_password"]:
                return import_status("ERROR_WRONG_PASSWORD", "FANSTI_ERROR", "ERROR_WRONG_PASSWORD")
            else:
                wechat_login = get_model_return_dict(self.susers.get_wechat_login(data["openid"]))
                make_log("wechat_login", wechat_login)
                if "login_name" not in data:
                    data["login_name"] = None
                if "name" not in data:
                    data["name"] = None
                if "usex" not in data:
                    data["usex"] = None
                if "city" not in data:
                    data["city"] = None
                if "province" not in data:
                    data["province"] = None
                add_wechat_login = add_model("WECHAT_LOGIN",
                                         **{
                                             "id": str(uuid.uuid1()),
                                             "login_name": data["login_name"],
                                             "openid": data["openid"],
                                             "status": "1",
                                             "phone": data["phone"],
                                             "name": data["name"],
                                             "usex": data["usex"],
                                             "city": data["city"],
                                             "province": data["province"]
                                         })
                make_log("add_wechat_login", add_wechat_login)
                if not add_wechat_login:
                    return SYSTEM_ERROR
        else:
            wechat_login = get_model_return_dict(self.susers.get_wechat_login(data["openid"]))
            make_log("wechat_login", wechat_login)
            add_wechat_login = add_model("WECHAT_LOGIN",
                                         **{
                                             "id": str(uuid.uuid1()),
                                             "openid": data["openid"],
                                             "status": "1",
                                             "phone": data["phone"],
                                              "name": data["name"],
                                              "usex": data["usex"],
                                              "city": data["city"],
                                              "province": data["province"]
                                         })
            make_log("add_wechat_login", add_wechat_login)
            if not add_wechat_login:
                return SYSTEM_ERROR

        return import_status("SUCCESS_USER_BINDING", "OK")

    def get_wechat_phone(self, phone):
        id = get_model_return_dict(self.susers.get_wechat_login_by_phone(phone))
        sm = []
        make_log("id", id)
        if "id" in id:
            return import_status("ERROR_SOMEONE_BINDING", "FANSTI_ERROR", "ERROR_SOMEONE_BINDING")
        try:
            import urllib2
            url = "https://shouji.supfree.net/fish.asp?cat={0}".format(phone)
            headers = {'Content-Type': 'application/xhtml+xml'}
            req = urllib2.Request(url, headers=headers)
            url_response = urllib2.urlopen(req)
            strResult = url_response.read()
            parser = MyHTMLParser()
            parser.feed(strResult)
            length = len(parser.text)
            while length >= 0:
                if parser.text[length - 1].replace(" ", "") in ["\r\n", "\r\n\r\n", "\r\n\r\n\r\n", "]", "?", "\r\n\t",
                                                                "\r\n\t\t", "\r\n\t\t\t", "\r\n\t\t\t\t'", ":", ">",
                                                                " ", ")"]:
                    parser.text.remove(parser.text[length - 1])
                elif "\r\n" in parser.text[length - 1] or "var" in parser.text[length - 1]:
                    parser.text.remove(parser.text[length - 1])
                length = length - 1

            for row in parser.text:
                if row.decode("gbk").encode("utf8") in ["归属地：", "号码段：", "卡类型：", "运营商："]:
                    sm.append(parser.text[parser.text.index(row) + 1])
        except Exception as e:
            print(e.message)
        if not sm:
            return import_status("ERROR_WRONG_TELPHONE", "FANSTI_ERROR", "ERROR_WRONG_TELPHONE")
        return 200


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
            response = import_status("ERROR_HAVE_BINDING", "OK")
            response["data"] = {}
            response["data"]["login_name"] = get_status_by_openid["login_name"]
            return response

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

    def make_user_message(self):
        args = request.args.to_dict()
        make_log("args", args)
        data = json.loads(request.data)
        make_log("data", data)
        true_args_params = ["openid"]
        true_data_params = ["message"]
        if judge_keys(true_args_params, args.keys()) != 200:
            return judge_keys(true_args_params, args.keys())
        if judge_keys(true_data_params, data.keys()) != 200:
            return judge_keys(true_data_params, data.keys())
        phone = get_model_return_dict(self.susers.get_wechat_login(args["openid"]))["phone"]
        new_message = add_model("USER_MESSAGE",
                                **{
                                    "id": str(uuid.uuid4()),
                                    "phone": phone,
                                    "message": data["message"]
                                })
        if not new_message:
            return SYSTEM_ERROR
        return import_status("SUCCESS_MAKE_MESSAGE", "OK")

    def get_user_message(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_args = ["page_size", "page_num"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        page_size = int(args.get("page_size"))
        page_num = int(args.get("page_num"))
        all_message = get_model_return_list(self.susers.get_user_message(page_size, page_num))
        make_log("all_message", all_message)
        response = import_status("SUCCESS_GET_RETRUE", "OK")
        response["data"] = {}
        response["data"]["message_list"] = all_message
        response["data"]["count"] = len(get_model_return_list(self.susers.get_all_user_message()))
        return response

    def add_invate(self):
        args = request.args.to_dict()
        make_log("args", args)
        data = json.loads(request.data)
        make_log("data", data)
        true_args = ["openid"]
        true_data = ["openid"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        if judge_keys(true_data, data.keys()) != 200:
            return judge_keys(true_data, data.keys())
        new_user_invate = add_model("USER_INVATE",
                                    **{
                                        "id": str(uuid.uuid4()),
                                        "args_openid": args["openid"],
                                        "invate_openid": data["openid"]
                                    })
        if not new_user_invate:
            return SYSTEM_ERROR
        return import_status("SUCCESS_NEW_INVATE", "OK")

    def get_invate_list(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_args = ["openid"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        all_invate = get_model_return_list(self.susers.get_invate_by_login_name(args["openid"]))
        make_log("all_invate", all_invate)
        for row in all_invate:
            a_invate = get_model_return_dict(self.susers.get_invate_abo_by_openid(row["invate_openid"]))
            make_log("a_invate", a_invate)
            if not a_invate:
                return SYSTEM_ERROR
            row["name"] = all_invate["name"]
            row["phone"] = all_invate["phone"]
        response = import_status("SUCCESS_GET_INVATE", "OK")
        response["data"] = all_invate
        return response

    def get_my_info(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_args = ["openid"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        my_info = get_model_return_dict(self.susers.get_personal_by_openid(args["openid"]))
        make_log("my_info", my_info)
        for row in my_info.keys():
            if my_info[row]:
                my_info[row] = my_info[row].decode("gbk").encode("utf8")
        response = import_status("SUCCESS_GET_RETRUE", "OK")
        response["data"] = my_info
        return response

    def update_my_info(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_args = ["openid"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        data = json.loads(request.data)
        make_log("data", data)
        true_data = ["user_name"]
        null_data = ["work_year", "work_goodat", "user_introduction", "qq", "wechat", "email"]
        if judge_keys(true_data, data.keys(), null_data) != 200:
            return judge_keys(true_data, data.keys(), null_data)
        phone = get_model_return_dict(self.susers.get_wechat_login(args["openid"]))["phone"]
        make_log("phone", phone)
        if not phone:
            return SYSTEM_ERROR
        my_info = get_model_return_dict(self.susers.get_personal_by_openid(args["openid"]))
        make_log("myinfo", my_info)
        if not my_info:
            return SYSTEM_ERROR
        for key in null_data:
            if key not in data.keys():
                data[key] = None
        update_info = self.susers.update_wechat_login(args["openid"],
                                                      {
                                                          "user_name": data["user_name"],
                                                          "work_year": data["work_year"],
                                                          "work_goodat": data["work_goodat"],
                                                          "user_introduction": data["user_introduction"],
                                                          "qq": data["qq"],
                                                          "wechat": data["wechat"],
                                                          "email": data["email"]
                                                      })
        if not update_info:
            return SYSTEM_ERROR
        response = import_status("SUCCESS_GET_RETRUE", "OK")
        return response

