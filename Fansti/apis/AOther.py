# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import json
import configparser
from flask_restful import Resource, request
from Fansti.config.response import APIS_WRONG
from Fansti.common.import_status import import_status
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list
from Fansti.config.Inforcode import FANSTICONFIG
class FSother(Resource):
    def __init__(self):
        self.title = "=========={0}=========="
        from Fansti.services.SUsers import SUsers
        self.suser = SUsers()
        from Fansti.services.SGoods import SGoods
        self.sgoods = SGoods()

    def get(self, other):
        print(self.title.format("api is" + other))
        if other == "get_custom":
            args = request.args.to_dict()
            make_log("args", args)
            true_params = ["login_name"]
            if judge_keys(true_params, args.keys()) != 200:
                return judge_keys(true_params, args.keys())

            if args["login_name"] not in ["", None]:
                accounts = get_model_return_dict(self.suser.get_compnay_by_loginname(args["login_name"]))
                if not accounts:
                    return import_status("ERROR_GET_CUSTOM", "FANSTI_ERROR", "ERROR_GET_CUSTOM")
                make_log("accounts", accounts)
                xsr = get_model_return_dict(self.sgoods.get_xsr_by_user(accounts["compnay"]))["xsr"]
                make_log("xsr", xsr)
                user_abo = get_model_return_dict(self.suser.get_custom_by_xsr(xsr))
                user_abo["user_name"] = user_abo["user_name"]
                make_log("user_abo", user_abo)
                data = user_abo
            else:
                cf = configparser.ConfigParser()
                cf.read(FANSTICONFIG)
                make_log("selector", cf.sections())
                name = cf.get("custom", "name")

                qq = cf.get("custom", "qq")
                telphone = cf.get("custom", "telphone")
                email = cf.get("custom", "email")
                data = {
                    "user_name": name.replace("\"", ""),
                    "qq": qq.replace("\"", ""),
                    "telephone": telphone.replace("\"", ""),
                    "email": email.replace("\"", "")
                }
            response = import_status("SUCCESS_GET_CUSTOM", "OK")
            response["data"] = data
            return response

        if other == "get_phone":
            cf = configparser.ConfigParser()
            cf.read(FANSTICONFIG)
            phone_list = cf.get("phone", "whitelist")
            if str(phone_list) == "[]":
                phone_list = str(phone_list).replace("[", "").replace("]", "")
                phone_list = list(phone_list)
            else:
                phone_list = str(phone_list).replace("[", "").replace("]", "").replace("\"", "") \
                    .replace("\'", "").replace("\\", "").replace(" ", "").replace("u", "").split(",")
                print(phone_list)
            response = import_status("SUCCESS_GET_NEWS", "OK")
            response["data"] = phone_list
            return response

        return APIS_WRONG

    def post(self, other):
        print(self.title.format("api is" + other))
        if other == "update_custom":
            data = json.loads(request.data)
            make_log("data", data)
            true_params = ["name", "qq", "telphone", "email"]
            if judge_keys(true_params, data.keys()) != 200:
                return judge_keys(true_params, data.keys())
            cf = configparser.ConfigParser()
            cf.read(FANSTICONFIG)
            cf.set("custom", "name", data["name"])
            cf.set("custom", "qq", data["qq"])
            cf.set("custom", "telphone", data["telphone"])
            cf.set("custom", "email", data["email"])
            cf.write(open(FANSTICONFIG, "w"))

            return import_status("SUCCESS_UPDATE_CUSTOM", "OK")

        if other == "update_phone":
            data = json.loads(request.data)
            true_params = ["control", "phone_list"]
            if judge_keys(true_params, data.keys()) != 200:
                return judge_keys(true_params, data.keys())
            cf = configparser.ConfigParser()
            cf.read(FANSTICONFIG)
            phone_list = cf.get("phone", "whitelist")
            for row in data["phone_list"]:
                if data["control"] == "delete":
                    if str(phone_list) == "[]":
                        phone_list = str(phone_list).replace("[", "").replace("]", "").replace("\r", "").replace("\n", "")\
                            .replace("\'", "")
                        phone_list = list(phone_list)
                    else:
                        phone_list = str(phone_list).replace("[", "").replace("]", "").replace("\"", "")\
                            .replace("\'", "").replace("\\", "").replace(" ", "").replace("u", "").split(",")
                        print(phone_list)
                    if row in phone_list:
                        phone_list.remove(row)
                if data["control"] == "add":
                    if str(phone_list) == "[]":
                        phone_list = str(phone_list).replace("[", "").replace("]", "")
                        phone_list = list(phone_list)
                    else:
                        phone_list = str(phone_list).replace("[", "").replace("]", "").replace("\"", "")\
                            .replace("\'", "").replace("\\", "").replace(" ", "").replace("u", "").split(",")
                        print(phone_list)
                    if row not in phone_list:
                        phone_list.append(row)
            print(phone_list)
            cf.set("phone", "whitelist", str(phone_list))
            cf.write(open(FANSTICONFIG, "w"))

            return import_status("SUCCESS_UPDATE_PHONE", "OK")
        return APIS_WRONG