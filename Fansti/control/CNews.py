# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import datetime, json, uuid
from Fansti.config.response import SYSTEM_ERROR, NETWORK_ERROR
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list
from Fansti.common.import_status import import_status
from Fansti.common.TransformToList import add_model

class CNews():
    def __init__(self):
        from Fansti.services.SNews import SNews
        self.snews = SNews()
        from Fansti.services.SUsers import SUsers
        self.susers = SUsers()

    def get_all(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_args = ["login_name", "page_size", "page_num"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        get_binding = get_model_return_dict(self.susers.get_wechat_login(args["login_name"]))
        make_log("get_binding", get_binding)
        if not get_binding:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")
        all_news = get_model_return_list(self.snews.get_all(args["page_num"], args["page_size"]))
        make_log("all_news", all_news)
        for news in all_news:
            news["news_time"] = news["news_time"].strftime("%Y-%m-%d %H:%M:%S")

        response = import_status("SUCCESS_GET_NEWS", "OK")
        response["data"] = all_news
        return response

    def get_abo(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_args = ["login_name", "id"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        get_binding = get_model_return_dict(self.susers.get_wechat_login(args["login_name"]))
        make_log("get_binding", get_binding)
        if not get_binding:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")
        one_news = get_model_return_dict(self.snews.get_message(args["id"]))
        make_log("one_news", one_news)
        one_news["news_time"] = one_news["news_time"].strftime("%Y-%m-%d %H:%M:%S")

        response = import_status("SUCCESS_GET_NEWS", "OK")
        response["data"] = one_news
        return response

    def new_news(self):
        data = json.loads(request.data)
        make_log("data", data)
        true_args = ["news_title", "news_all", "news_picture", "news_from"]
        if judge_keys(true_args, data.keys()) != 200:
            return judge_keys(true_args, data.keys())
        new_news = add_model("WECHAT_NEWS",
                             **{
                                 "id": str(uuid.uuid4()),
                                 "news_title": data["news_title"],
                                 "news_all": data["news_all"],
                                 "news_picture": data["news_picture"],
                                 "news_from": data["news_from"],
                                 "news_status": "1",
                                 "news_time": datetime.datetime.now()
                             })
        if not new_news:
            return SYSTEM_ERROR
        return import_status("SUCCESS_NEW_NEWS", "OK")

    def update_news(self):
        pass