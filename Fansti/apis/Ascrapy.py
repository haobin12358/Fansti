# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from Fansti.config.response import APIS_WRONG

class FSscrapy(Resource):
    def __init__(self):
        self.title = "=========={0}=========="
        from Fansti.control.Cscrapy import Cscrapy
        self.cscrapy = Cscrapy()

    def get(self, scrapy):
        print(self.title.format("api is" + scrapy))

        apis = {
            "get_hs": "self.cscrapy.get_hs()",
            "get_cas": "self.cscrapy.get_cas()",
            "get_jd": "self.cscrapy.get_jd()",
            "get_flyno": "self.cscrapy.get_flyno()",
            "get_all_scrapy": "self.cscrapy.get_all_scrapy()",
            "get_dgr": "self.cscrapy.get_dgr()",
            "get_tact": "self.cscrapy.get_tact()"
        }

        if scrapy not in apis:
            return APIS_WRONG
        return eval(apis[scrapy])

    def post(self, scrapy):
        print(self.title.format("api is" + scrapy))

        apis = {
            "update_airline": "self.cscrapy.new_update_airline()",
            "upload_dgr": "self.cscrapy.upload_template_dgr()",
        }

        if scrapy not in apis:
            return APIS_WRONG
        return eval(apis[scrapy])