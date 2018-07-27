# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from Fansti.config.response import APIS_WRONG

class FSGoods(Resource):
    def __init__(self):
        self.title = "=========={0}=========="
        from Fansti.control.CGoods import CGoods
        self.cgoods = CGoods()

    def get(self, goods):
        print(self.title.format("api is" + goods))

        apis = {
            "get_goods_list": "self.cgoods.get_goods_list()",
            "get_jc_abo": "self.cgoods.get_jc_abo()"
        }

        if goods not in apis:
            return APIS_WRONG
        return eval(apis[goods])
