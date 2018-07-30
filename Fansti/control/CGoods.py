# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import json
from flask import request
from Fansti.config.response import SYSTEM_ERROR
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list
from Fansti.common.import_status import import_status

class CGoods():
    def __init__(self):
        from Fansti.services.SGoods import SGoods
        self.sgoods = SGoods()
        from Fansti.services.SUsers import SUsers
        self.susers = SUsers()

    def get_goods_list(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name']
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        accounts = get_model_return_dict(self.susers.get_compnay_by_loginname(args["login_name"]))
        make_log("accounts", accounts)
        goods_list = get_model_return_list(self.sgoods.get_all_goods_by_user(accounts["compnay"]))
        make_log("goods_list", goods_list)
        for goods in goods_list:
            yupei = get_model_return_dict(self.sgoods.get_dctime_by_jcno(goods["jcno"]))
            make_log("yupei", yupei)
            if not yupei or not yupei["dctime"]:
                goods["yupei"] = "0"
            else:
                goods["yupei"] = "1"
            jincang = get_model_return_list(self.sgoods.get_in_order_by_jcno(goods["jcno"]))
            make_log("jincang", jincang)
            if not jincang or not jincang["photourl"]:
                goods["jincang"] = "0"
            else:
                goods["jincang"] = "1"
            chucang = get_model_return_list(self.sgoods.get_out_order_by_jcno(goods["jcno"]))
            make_log("chucang", chucang)
            if not chucang or not chucang["photourl"]:
                goods["chucang"] = "0"
            else:
                goods["chucang"] = "1"
            chengzhong = get_model_return_list(self.sgoods.get_weight_order_by_jcno(goods["jcno"]))
            make_log("chengzhong", chengzhong)
            if not chengzhong or not chengzhong["photourl"]:
                goods["chengzhong"] = "0"
            else:
                goods["chengzhong"] = "1"
            baoguan = get_model_return_list(self.sgoods.get_content_by_jcno(goods["jcno"]))
            make_log("baoguan", baoguan)
            if not baoguan or not baoguan["content"]:
                goods["baoguan"] = "0"
            else:
                goods['baoguan'] = "1"
            yundan = get_model_return_list(self.sgoods.get_awb_by_jcno(goods["jcno"]))
            make_log("yundan", yundan)
            if not yundan or not yundan["content"]:
                goods["yundan"] = "0"
            else:
                goods["yundan"] = "1"
            jiaodan = get_model_return_dict(self.sgoods.get_jd_by_jcno(goods["jcno"]))
            make_log("jiaodan", jiaodan)
            if not jiaodan:
                goods["jiaodan"] = "0"
            else:
                if not jiaodan["jd_date"] and not jiaodan["jd_time"]:
                    goods["jiaodan"] = "0"
                else:
                    goods["jiaodan"] = "1"
            qifei = get_model_return_dict(self.sgoods.get_hbdate_by_jcno(goods["jcno"]))
            make_log("qifei", qifei)
            if not qifei or not qifei["hbdate1"]:
                goods["qifei"] = "0"
            else:
                goods["qifei"] = "1"
            dida = get_model_return_dict(self.sgoods.get_dhmes_by_jcno(goods["jcno"]))
            make_log("dida", dida)
            if not dida or not dida["dhmes"]:
                goods["dida"] = "0"
            else:
                goods["dida"] = "1"
        print goods_list
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

        jc_abo = get_model_return_dict(self.sgoods.get_goods_abo_by_jcno(args["jcno"]))
        make_log("jc_abo", jc_abo)
        if not jc_abo:
            return SYSTEM_ERROR
        quantity_weight = get_model_return_dict(self.sgoods.get_quantity_weight_by_jcno(args["jcno"]))
        make_log("quantity_weight", quantity_weight)
        if not quantity_weight:
            return SYSTEM_ERROR
        jc_abo["quantity"] = quantity_weight["quantity"]
        jc_abo["weight"] = quantity_weight["weight"]
        jc_abo["in"] = {}
        jc_abo["in"]["picture"] = []
        jc_abo["out"] = {}
        jc_abo["out"]["picture"] = []
        jc_abo["weight"] = {}
        jc_abo["weight"]["picture"] = []
        jc_abo_in = get_model_return_list(self.sgoods.get_in_order_by_jcno(args["jcno"]))
        make_log("jc_abo_in", jc_abo_in)
        if jc_abo_in:
            for in_order in jc_abo_in:
                jc_abo["in"]["createtime"] = in_order["createtime"].strftime("%Y-%m-%d")
                jc_abo["in"]["czr"] = in_order["czr"].decode("gbk").encode("utf8")
                jc_abo["in"]["picture"].append(in_order["photourl"])
        jc_abo_out = get_model_return_list(self.sgoods.get_out_order_by_jcno(args["jcno"]))
        make_log("jc_abo_out", jc_abo_out)
        if jc_abo_out:
            for out_order in jc_abo_out:
                jc_abo["out"]["createtime"] = out_order["createtime"].strftime("%Y-%m-%d")
                jc_abo["out"]["czr"] = out_order["czr"].decode("gbk").encode("utf8")
                jc_abo["out"]["picture"].append(out_order["photourl"])
        jc_abo_weight = get_model_return_list(self.sgoods.get_in_order_by_jcno(args["jcno"]))
        make_log("jc_abo_weight", jc_abo_weight)
        if jc_abo_weight:
            for weight_order in jc_abo_weight:
                jc_abo["weight"]["createtime"] = weight_order["createtime"].strftime("%Y-%m-%d")
                jc_abo["weight"]["czr"] = weight_order["czr"].decode("gbk").encode("utf8")
                jc_abo["weight"]["picture"].append(weight_order["photourl"])

        response = import_status("SUCCESS_GET_JC", "OK")
        response["data"] = jc_abo
        return response