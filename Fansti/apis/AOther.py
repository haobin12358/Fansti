# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import ConfigParser, json
from flask_restful import Resource, request
from Fansti.config.response import APIS_WRONG
from Fansti.common.import_status import import_status
from Fansti.common.Log import make_log, judge_keys

class FSother(Resource):
    def __init__(self):
        self.title = "=========={0}=========="

    def get(self, other):
        print(self.title.format("api is" + other))
        if other == "get_custom":
            cf = ConfigParser.ConfigParser()
            cf.read("../Fansti/fansticonfig.ini")
            name = cf.get("custom", "name")
            qq = cf.get("custom", "qq")
            telphone = cf.get("custom", "telphone")
            email = cf.get("custom", "email")
            data = {
                "name": name.replace("\"", ""),
                "qq": qq.replace("\"", ""),
                "telphone": telphone.replace("\"", ""),
                "email": email.replace("\"", "")
            }
            response = import_status("SUCCESS_GET_CUSTOM", "OK")
            response["data"] = data
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
            cf = ConfigParser.ConfigParser()
            cf.read("../Fansti/fansticonfig.ini")
            cf.set("custom", "name", data["name"])
            cf.set("custom", "qq", data["qq"])
            cf.set("custom", "telphone", data["telphone"])
            cf.set("custom", "email", data["email"])
            cf.write(open("../Fansti/fansticonfig.ini", "r+"))

            return import_status("SUCCESS_UPDATE_CUSTOM", "OK")