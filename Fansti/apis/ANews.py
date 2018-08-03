# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from Fansti.config.response import APIS_WRONG

class FSNews(Resource):
    def __init__(self):
        self.title = "=========={0}=========="
        from Fansti.control.CNews import CNews
        self.cnews = CNews()

    def get(self, news):
        print(self.title.format("api is" + news))

        apis = {
            "get_all": "self.cnews.get_all()",
            "get_abo": "self.cnews.get_abo()"
        }

        if news not in apis:
            return APIS_WRONG
        return eval(apis[news])

    def post(self, news):
        print(self.title.format("api is" + news))

        apis = {
            "new_news": "self.cnews.new_news()",
            "update_news": "self.cnews.update_news()",
            "upload_files": "self.cnews.upload_files()"
        }

        if news not in apis:
            return APIS_WRONG
        return eval(apis[news])