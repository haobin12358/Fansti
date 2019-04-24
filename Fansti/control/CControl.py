# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import json, uuid, datetime
from flask import request
from Fansti.config.response import SYSTEM_ERROR
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list
from Fansti.common.import_status import import_status
from Fansti.common.TransformToList import add_model

class CControl():
    def __init__(self):
        from Fansti.services.SGoods import SGoods
        self.sgoods = SGoods()
        from Fansti.services.SUsers import SUsers
        self.susers = SUsers()

    def get_today_list(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "page_size", "page_num", "time_use"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        wts_filter = set()
        from Fansti.models.model import AIR_HWYS_WTS

        user = self.susers.get_user_type(args.get("login_name"))
        if not user:
            return import_status("ERROR_NONE_USER", "FANSTI_ERROR", "ERROR_NONE_USER")
        usertype = user.user_type
        if usertype:
            try:
                usertype = int(usertype)
            except Exception as e:
                make_log('get good list error', e)
                return SYSTEM_ERROR

        # 根据usertype判断login_name的场景
        from sqlalchemy import or_
        if usertype == 10:
            wts_filter.add(or_(AIR_HWYS_WTS.czr == args.get("login_name"), AIR_HWYS_WTS.xsr == args.get("login_name")))
        elif usertype == 0:
            pass
        else:
            accounts = get_model_return_dict(self.susers.get_compnay_by_loginname(args["login_name"]))
            make_log("accounts", accounts)
            wts_filter.add(AIR_HWYS_WTS.accounts == accounts.get("compnay"))
        # 处理当前时间
        if args["time_use"] == 0:
            today_date = datetime.datetime.now().date()
            wts_filter.add(or_(AIR_HWYS_WTS.jd_time.date() == today_date, AIR_HWYS_WTS.jd_date == today_date))
        elif args["time_use"] == 1:
            pass
        goods_list = get_model_return_list(self.sgoods.get_all_goods_by_filter(
            wts_filter, int(args["page_size"]), int(args["page_num"])))

        for row in goods_list:
            if row["flag_date"]:
                row["flag_date"] = row["flag_date"].strftime("%Y-%m-%d")
                row["backcolor"] = "灰色"
            if row["transtime"]:
                if row["transtime"] == datetime.datetime.now().date():
                    row["backcolor"] = "黄色"
                else:
                    row["backcolor"] = "白色"
                row["transtime"] = row["transtime"].strftime("%Y-%m-%d")
            if "backcolor" not in row.keys():
                row["backcolor"] = "白色"
            if row["isphoto"]:
                row["backcolor"] = "红色"
                if row["isphoto"] == "直接交货！":
                    row["icon"] = "交货"
                elif row["isphoto"] == "拍照等确认！":
                    row["icon"] = "拍照"
            else:
                row["icon"] = None

        make_log("goods_list", goods_list)
        response = import_status("SUCCESS_GET_GOODS", "OK")
        response["data"] = goods_list
        return response

    def get_jc_abo(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")

        jc_abo = get_model_return_dict(self.sgoods.get_control_goods(args["jcno"]))

        dzjjd = get_model_return_dict(self.sgoods.get_dzjjd(args["jcno"]))
        if dzjjd:
            jc_abo["wh_require"] = jc_abo["wh_require"] or dzjjd["kf_bz"]
            jc_abo["instruction"] = jc_abo["instruction"] or dzjjd["hc_bz"]
        jc_abo["jd_date"] = jc_abo["jd_date"] or jc_abo["jd_time"]
        jc_abo["jd_time"] = None
        if jc_abo["arrivetime"]:
            jc_abo["arrivetime"] = jc_abo["arrivetime"].strftime("%Y/%m/%d")
        if jc_abo["jd_date"]:
            jc_abo["jd_date"] = jc_abo["jd_date"].strftime("%Y/%m/%d")
            jc_abo["show_button"] = 0
        else:
            jc_abo["show_button"] = 1

        # TODO 缺失航班日期
        dcd = get_model_return_dict(self.sgoods.get_dcd_flight(args["jcno"]))
        if dcd:
            jc_abo["contract"] = dcd["flight"]
            jc_abo["contract_time"] = dcd["hbdate1"] or dcd["flightdate"]
            if jc_abo["contract_time"]:
                jc_abo["contract_time"] = jc_abo["contract_time"].strftime("%Y/%m/%d")
        else:
            jc_abo["contract"] = None
            jc_abo["contract_time"] = None
        response = import_status("SUCCESS_GET_JC", "OK")
        response["data"] = jc_abo
        return response
