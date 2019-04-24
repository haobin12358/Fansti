# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from Fansti.config.response import APIS_WRONG

class FSRed(Resource):
    def __init__(self):
        self.title = "=========={0}=========="
        from Fansti.control.CReds import CReds
        self.creds = CReds()

    def get(self, reds):
        print(self.title.format("api is" + reds))

        apis = {
            "get_all_red": "self.creds.get_all_red()"
        }

        if reds not in apis:
            return APIS_WRONG
        return eval(apis[reds])

    def post(self, reds):
        print(self.title.format("api is" + reds))

        apis = {
            "receive_red": "self.creds.receive_red()",
            "receive_red_query": "self.creds.receive_red_query()"
        }

        if reds not in apis:
            return APIS_WRONG
        return eval(apis[reds])