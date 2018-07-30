# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import datetime, calendar, json
from flask import request
from Fansti.config.response import SYSTEM_ERROR, NETWORK_ERROR
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list
from Fansti.common.import_status import import_status
from Fansti.common.TransformToList import add_model

class CReds():
    def __init__(self):
        from Fansti.services.SReds import SReds
        self.sred = SReds()

    def get_all_red(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_params = ["login_name"]
        if judge_keys(true_params, args.keys()) != 200:
            return judge_keys(true_params, args.keys())
        all_red = get_model_return_list(self.sred.get_my_red_status(args["login_name"]))
        make_log("all_red", all_red)
        response = import_status("SUCCESS_GET_RED", "OK")
        response["data"] = {}
        response["data"]["red_list"] = []
        for red in all_red:
            red_id = red["red_id"]
            red_abo = get_model_return_dict(self.sred.get_red_by_id(red_id))
            make_log("red_abo", red_abo)
            if not red_abo:
                return SYSTEM_ERROR
            red_abo["name"] = red_abo["name"].decode("gbk").encode("utf8")
            #red["createtime"] = red["createtime"].strftime("%Y-%m-%d")
            response["data"]["red_list"].append(red_abo)
        response["data"]["red_num"] = len(get_model_return_list(self.sred.get_my_red_rereceive(args["login_name"])))
        response["data"]["red_list"] = all_red
        my_red = get_model_return_list(self.sred.get_my_red_receive(args["login_name"]))
        response["data"]["my_red_num"] = len(my_red)
        all_price = 0
        for red in my_red:
            a_red = get_model_return_dict(self.sred.get_red_by_id(red["red_id"]))
            make_log("a_red", a_red)
            red["createtime"] = red["createtime"].strftime("%Y-%m-%d")
            if not a_red:
                return SYSTEM_ERROR
            a_red["name"] = a_red["name"].decode("gbk").encode("utf8")
            all_price = all_price + float(a_red["price"])

        response["data"]["my_red_list"] = my_red
        response["data"]["my_red_coin"] = all_price
        response["data"]["month_red"] = []
        month = 1
        while month < 13:
            my_red_month = get_model_return_list(self.sred.get_my_red_by_time(
                datetime.datetime(datetime.datetime.now().year, month, 1, 0, 0, 0),
                datetime.datetime(datetime.datetime.now().year, month, calendar.monthrange(
                    datetime.datetime.now().year, month)[1], 23, 59, 59)
            ))
            month_red = {
                "month": month,
                "count": len(my_red_month)
            }
            response["data"]["month_red"].append(month_red)
            month = month + 1
        print(response)
        return response

    def receive_red(self):
        args = request.args.to_dict()

        data = json.loads(request.data)