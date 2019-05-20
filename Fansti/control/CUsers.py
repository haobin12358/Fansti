# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import json, uuid, re
from flask import request
from flask import make_response
from Fansti.config.response import SYSTEM_ERROR, NETWORK_ERROR
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list
from Fansti.common.import_status import import_status
from Fansti.common.TransformToList import add_model
from html.parser import HTMLParser

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
        wl_key = ['status', 'openid', 'province', 'name', 'user_introduction', 'city',
                  'work_goodat', 'qq', 'login_name', 'work_year', 'phone', 'email',
                  'wechat', 'user_name', 'id', 'usex']

        wl = {k: data.get(k) for k in wl_key if k in data}
        import configparser
        from Fansti.config.Inforcode import FANSTICONFIG
        cfg = configparser.ConfigParser()
        cfg.read(FANSTICONFIG)
        usertype = -111
        phone_list = eval(cfg.get("phone", "whitelist"))
        data["name"] = None
        if str(data.get("phone")) in phone_list:
            wechat_login_tmp = get_model_return_dict(self.susers.get_wechat_login_by_phone(data.get("phone")))
            if not wechat_login_tmp:
                if "login_name" in data and "login_password" in data:
                    check_result = self.check_name_password(data.get("login_name"), data.get("login_password"))
                    if check_result:
                        return check_result

                self.susers.add_model("WECHAT_LOGIN", **{
                    "id": str(uuid.uuid1()),
                    "openid": data.get("openid", ""),
                    "login_name": data.get("login_name", ""),
                    "name": data.get("name", ""),
                    "phone": data.get("phone"),
                    "status": data.get("status", "1"),
                    "usex": data.get("usex", ""),
                    "city": data.get("city", ""),
                    "province": data.get("province", "")
                })

            else:
                if "login_name" in data and "login_password" in data:
                    check_result = self.check_name_password(data.get("login_name"), data.get("login_password"))
                    if check_result:
                        return check_result
                    usertype = get_model_return_dict(self.susers.get_user_type(data.get("login_name"))).get("user_type")
                update_result = self.susers.update_wechat_login_by_phone(data.get("phone"), wl)
                if not update_result:
                    return import_status("ERROR_UPDATE_DATA", "FANSTI_ERROR", "ERROR_UPDATE_DATA")
            response = import_status("SUCCESS_USER_BINDING", "OK")
            response['data'] = usertype
            return response
        if judge_keys(true_data, data.keys(), null_data) != 200:
            return judge_keys(true_data, data.keys(), null_data)
        # if self.get_wechat_phone(data["phone"]) != 200:
            # return self.get_wechat_phone(data["phone"]
        wl_tmp = get_model_return_dict(self.susers.get_wechat_login_by_phone(data["phone"]))

        if "login_name" in data and "login_password" in data:
            check_result = self.check_name_password(data.get("login_name"), data.get("login_password"))
            if check_result:
                return check_result
            usertype = get_model_return_dict(self.susers.get_user_type(data.get("login_name"))).get("user_type")

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
        if "id" in wl_tmp:
            self.susers.update_wechat_login_by_phone(data['phone'], wl)
        else:
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
        # else:
        #     add_wechat_login = add_model("WECHAT_LOGIN",
        #                                  **{
        #                                      "id": str(uuid.uuid1()),
        #                                      "openid": data["openid"],
        #                                      "status": "1",
        #                                      "phone": data["phone"],
        #                                       "name": data["name"],
        #                                       "usex": data["usex"],
        #                                       "city": data["city"],
        #                                       "province": data["province"]
        #                                  })
        #     make_log("add_wechat_login", add_wechat_login)
        #     if not add_wechat_login:
        #         return SYSTEM_ERROR
        response = import_status("SUCCESS_USER_BINDING", "OK")
        from Fansti.config.Inforcode import FANSTICONFIG
        import configparser
        cf = configparser.ConfigParser()
        cf.read(FANSTICONFIG)
        phone_list = cf.get("enquiry", "whitelist")
        if str(phone_list) == "[]":
            phone_list = str(phone_list).replace("[", "").replace("]", "")
            phone_list = list(phone_list)
        else:
            phone_list = str(phone_list).replace("[", "").replace("]", "").replace("\"", "") \
                .replace("\'", "").replace("\\", "").replace(" ", "").replace("u", "").split(",")
            print(phone_list)
        response["data"] = {}
        response['data']["user_type"] = usertype
        if data["login_name"] not in phone_list:
            response["data"]["is_show"] = 0
        else:
            response["data"]["is_show"] = 1
        return response

    def get_wechat_phone(self, phone):
        id = get_model_return_dict(self.susers.get_wechat_login_by_phone(phone))
        make_log("id", id)
        if "id" in id and not id["login_name"]:
            return import_status("ERROR_SOMEONE_BINDING", "FANSTI_ERROR", "ERROR_SOMEONE_BINDING")
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
            return SYSTEM_ERROR
        else:
            if not get_status_by_openid["login_name"]:
                user_type = -111
            else:
                user_type = get_model_return_dict(self.susers.get_user_type(get_status_by_openid["login_name"]))["user_type"]

        from Fansti.config.Inforcode import FANSTICONFIG
        import configparser
        cf = configparser.ConfigParser()
        cf.read(FANSTICONFIG)
        phone_list = cf.get("enquiry", "whitelist")
        if str(phone_list) == "[]":
            phone_list = str(phone_list).replace("[", "").replace("]", "")
            phone_list = list(phone_list)
        else:
            phone_list = str(phone_list).replace("[", "").replace("]", "").replace("\"", "") \
                .replace("\'", "").replace("\\", "").replace(" ", "").replace("u", "").split(",")
            print(phone_list)

        
        response = import_status("ERROR_HAVE_BINDING", "OK")
        response["data"] = {}
        if get_status_by_openid["login_name"] not in phone_list:
            response["data"]["is_show"] = 0
        else:
            response["data"]["is_show"] = 1
        response["data"]["login_name"] = get_status_by_openid["login_name"]
        response["data"]["user_type"] = user_type
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
            import urllib.request
            req = urllib.request.urlopen(request_url)
            strResult = req.read().decode("utf8")
            req.close()
            make_log("strResult", strResult)
        except Exception as e:
            print(e)
            return NETWORK_ERROR
        jsonResult = json.loads(strResult)
        if "openid" not in strResult or "session_key" not in strResult:
            return jsonResult
        openid = jsonResult["openid"]
        response = import_status("SUCCESS_GET_OPENID", "OK")
        response["data"] = {}
        response["data"]["openid"] = openid
        return response

    def get_openid2(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_params = ["code"]
        if judge_keys(true_params, args.keys()) != 200:
            return judge_keys(true_params, args.keys())
        request_url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type={3}" \
            .format("wxd1facdac814bb86f", "d92626eb3dc8e0e0f1cff7d511d28b0a", args["code"], "authorization_code")
        strResult = None
        try:
            import urllib.request
            req = urllib.request.urlopen(request_url)
            strResult = req.read().decode("utf8")
            req.close()
            make_log("strResult", strResult)
        except Exception as e:
            print(e)
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
        wechat_login = get_model_return_dict(self.susers.get_wechat_login_by_openid(data["openid"]))
        user_invate = get_model_return_dict(self.susers.get_id_by_openid(data["openid"]))
        if user_invate:
            return import_status("ERROR_MESSAGE_CLICK", "FANSTI_ERROR", "ERROR_HAVE_INVATED")
        if wechat_login:
            return import_status("ERROR_HAVE_INVATED", "FANSTI_ERROR", "ERROR_HAVE_INVATED")
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
        true_args = ["openid", "page_size", "page_num"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        all_invate = get_model_return_list(self.susers.get_invate_by_login_name(args["openid"], int(args["page_size"]), int(args["page_num"])))
        make_log("all_invate", all_invate)
        for row in all_invate:
            a_invate = get_model_return_dict(self.susers.get_invate_abo_by_openid(row["invate_openid"]))
            if a_invate:
                make_log("a_invate", a_invate)
                row["name"] = a_invate["name"]
                    #.decode("gbk").encode("utf8")
                row["phone"] = a_invate["phone"]

        phone = get_model_return_dict(self.susers.get_wechat_login(args["openid"]))
        make_log("phone", phone)
        if not phone:
            return SYSTEM_ERROR
        phone = phone["phone"]
        response = import_status("SUCCESS_GET_INVATE", "OK")
        top_phone = args.get("top_phone")

        if top_phone:
            phone = top_phone

        if self.check_role(phone):
            response["top_phone"] = phone
            for row in all_invate:
                invate_openid = row["invate_openid"]
                second_all_invate = get_model_return_list(self.susers.get_invate_by_login_name(invate_openid, int(args["page_size"]), int(args["page_num"])))
                make_log("second_all_invate", second_all_invate)
                row["second_invate"] = False
                if second_all_invate:
                    row["second_invate"] = True

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
                my_info[row] = my_info[row]
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

    def check_name_password(self, name, password):
        # TODO 判断是否存在当前月红包，存在的话
        import hashlib
        login_password = hashlib.md5()
        login_password.update(password.encode("utf8"))
        password = login_password.hexdigest()
        name_password_phone = get_model_return_dict(self.susers.get_name_password_phone(name))
        make_log("name_password_phone", name_password_phone)
        if not name_password_phone:
            return import_status("ERROR_NONE_USER", "FANSTI_ERROR", "ERROR_NONE_USER")
        if password != name_password_phone["login_password"]:
            return import_status("ERROR_WRONG_PASSWORD", "FANSTI_ERROR", "ERROR_WRONG_PASSWORD")
        else:
            # 用户名密码没问题 增加红包
            red_conis = self.sreds.get_red_all()
            for red_coin in red_conis:
                my_red_coin = self.sreds.get_myred_by_redid(red_coin.id)
                if my_red_coin:
                    continue
                import datetime
                self.sreds.add_model("GET_RED_COIN", **{
                    "id": str(uuid.uuid1()),
                    "login_name": name,
                    "createtime": datetime.datetime.now(),
                    "red_id": red_coin.id,
                    "status": 0
                })

            return False

    def check_username_phone(self, name, phone):
        name_password_phone = get_model_return_dict(self.susers.get_name_password_phone(name))
        if name_password_phone and name_password_phone["phone"] == phone:
            return True
        else:
            return False


    def check_role(self, phone):
        import configparser
        from Fansti.config.Inforcode import FANSTICONFIG
        cf = configparser.ConfigParser()
        cf.read(FANSTICONFIG)
        phone_list = cf.get("phone", "whitelist")
        if str(phone_list) == "[]":
            phone_list = str(phone_list).replace("[", "").replace("]", "")
            phone_list = list(phone_list)
        else:
            phone_list = str(phone_list).replace("[", "").replace("]", "").replace("\"", "") \
                .replace("\'", "").replace("\\", "").replace(" ", "").replace("u", "").split(",")

        return phone in phone_list

    def user_login_local(self):
        data = json.loads(request.data)
        make_log("data", data)
        true_data = ["phone", "login_name", "login_password"]
        if judge_keys(true_data, data.keys()) != 200:
            return judge_keys(true_data, data.keys())

        if "login_name" in data and "login_password" in data:
            check_result = self.check_name_password(data.get("login_name"), data.get("login_password"))
            if check_result:
                return check_result
        usertype = get_model_return_dict(self.susers.get_user_type(data.get("login_name"))).get("user_type")
        if not self.check_username_phone(data["login_name"], data["phone"]):
            return {
                "status": 405,
                "status_code": 405601,
                "message": "手机号错误"
            }
        return {
            "status": 200,
            "message": "登陆成功",
            "data": {
                "user_type": usertype
            }
        }