# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from Fansti.config.response import APIS_WRONG

class FSUser(Resource):
    def __init__(self):
        self.title = "=========={0}=========="
        from Fansti.control.CUsers import CUsers
        self.cusers = CUsers()

    def get(self, users):
        print(self.title.format("api is" + users))

        apis = {
            "get_binding": "self.cusers.get_binding()",
            "get_openid": "self.cusers.get_openid()",
            "get_invate_list": "self.cusers.get_invate_list()",
            "get_user_message": "self.cusers.get_user_message()",
            "get_my_info": "self.cusers.get_my_info()"
        }

        if users not in apis:
            return APIS_WRONG
        return eval(apis[users])

    def post(self, users):
        print(self.title.format("api is" + users))

        apis = {
            "user_binding": "self.cusers.user_binding()",
            "make_user_message": "self.cusers.make_user_message()",
            "add_invate": "self.cusers.add_invate()",
            "update_my_info": "self.cusers.update_my_info()"
        }

        if users not in apis:
            return APIS_WRONG
        return eval(apis[users])