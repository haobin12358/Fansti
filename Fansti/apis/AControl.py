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
            "get_jc_pic": "self.cgoods.get_jc_pic()",
            "get_jc_cb": "self.cgoods.get_jc_cb()",
            "get_fkdw": "self.cgoods.get_fkdw()",
            "get_fyzl": "self.cgoods.get_fyzl()",
            "get_in_abo": "self.cgoods.get_in_abo()",
            "get_out_abo": "self.cgoods.get_out_abo()",
            "get_hc_abo": "self.cgoods.get_hc_abo()",
            "get_sb_list": "self.cgoods.get_sb_list()",
            "get_bzsm_list": "self.cgoods.get_bzsm_list()",
            "get_jd_list": "self.cgoods.get_jd_list()",
            "get_sbno_list": "self.cgoods.get_sbno_list()"
        }

        if control not in apis:
            return APIS_WRONG
        return eval(apis[control])

    def post(self, control):
        print(self.title.format("api is " + control))

        apis = {
            "update_dzjjd": "self.cgoods.update_dzjjd()",
            "upload_files": "self.cgoods.upload_files()"
        }

        if control not in apis:
            return APIS_WRONG
        return eval(apis[control])