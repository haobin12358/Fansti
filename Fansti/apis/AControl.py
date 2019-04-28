# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from Fansti.config.response import APIS_WRONG

class FSControl(Resource):
    def __init__(self):
        self.title = "=========={0}=========="
        from Fansti.control.CControl import CControl
        self.cgoods = CControl()

    def get(self, control):
        print(self.title.format("api is" + control))

        apis = {
            "get_today_list": "self.cgoods.get_today_list()",
            "get_jc_abo": "self.cgoods.get_jc_abo()",
            "get_handover_list": "self.cgoods.get_handover_list()",
            "get_jc_pic": "self.cgoods.get_jc_pic()"
        }

        if control not in apis:
            return APIS_WRONG
        return eval(apis[control])

    def post(self, control):
        print(self.title.format("api is " + control))

        apis = {
            "retrue_goods": "self.cgoods.retrue_goods()"
        }

        if control not in apis:
            return APIS_WRONG
        return eval(apis[control])