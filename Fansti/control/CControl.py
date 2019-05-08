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
        not_null_params = ['login_name', "page_size", "page_num", "time_use", "select_name"]
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
        if args["select_name"]:
            wts_filter.add(or_(AIR_HWYS_WTS.jcno.like("%{0}%".format(args["select_name"])),
                               AIR_HWYS_WTS.ydno.like("%{0}%".format(args["select_name"])),
                               AIR_HWYS_WTS.destination.like("%{0}%".format(args["select_name"]))))
        # 处理当前时间 时间格式为2019-04-29
        if args["time_use"]:
            args["time_use"] = datetime.datetime.strptime(args["time_use"], "%Y-%m-%d")
            today_date = datetime.datetime.now().date()
            wts_filter.add(or_(AIR_HWYS_WTS.jd_time.date() == today_date, AIR_HWYS_WTS.jd_date == today_date))

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

        user_type = get_model_return_dict(self.susers.get_user_type(args["login_name"]))["user_type"]
        if user_type in ["0", "3", "4"]:
            royaltys = get_model_return_list(self.sgoods.get_royalty_by_jcno(args["jcno"]))
            for row in royaltys:
                jc_abo["packer_leader"] = row["packer_leader"]
            jc_abo["packer_list"] = royaltys
            if user_type == "4" and not royaltys:
                jc_abo["save_button"] = 1
            else:
                jc_abo["save_button"] = 0
        elif user_type in ["5"]:
            royaltys = get_model_return_list(self.sgoods.get_royalty_by_jcno(args["jcno"]))
            for row in royaltys:
                jc_abo["packer_leader"] = row["packer_leader"]
                if row["packer_confrim"] == "是":
                    jc_abo["retrue_packer_button"] = 0
                else:
                    jc_abo["retrue_packer_button"] = 1
                if row["packer_ok"] == "是":
                    jc_abo["retrue_ok_button"] = 0
                else:
                    jc_abo["retrue_ok_button"] = 1
            jc_abo["packer_list"] = royaltys


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

    def get_handover_list(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")

        handover_list = get_model_return_dict(self.sgoods.get_wts_handover(args["jcno"]))
        dzjjd_handover = self.sgoods.get_dzjjd_handover(args["jcno"])
        if dzjjd_handover:
            handover_list.update(get_model_return_dict(dzjjd_handover))
        else:
            handover_list.update({
                "kfqr_date": None,
                "hcqr_date": None,
                "rkd_flag": None,
                "ungoods_flag": None,
                "sjwj_flag": None,
                "goods_file": None,
                "tp_mass": None,
                "state_goods": None,
                "tp_size": None,
                "temperature": None,
                "dtp": None,
                "gb_flag": None,
                "gb_num": None,
                "lb_flag": None,
                "lb_num": None,
                "in_mark": None,
                "out_mark": None,
                "ybzbl_flag": None,
                "nbzsm": None,
                "bzpm": None,
                "kf_ry": None,
                "kf_bz": None,
                "hc_ry": None,
                "hc_bz": None
            })

        # 库房确认时间/货场确认时间处理
        if handover_list["kfqr_date"]:
            handover_list["kfqr_date"] = handover_list["kfqr_date"].strftime("%Y-%m-%d %H:%M:%S")
            handover_list["kf_button"] = 0
        else:
            handover_list["kfqr_date"] = "没有确认"
            handover_list["kf_button"] = 1

        if handover_list["hcqr_date"]:
            handover_list["hcqr_date"] = handover_list["hcqr_date"].strftime("%Y-%m-%d %H:%M:%S")
            handover_list["hc_button"] = 0
        else:
            handover_list["hcqr_date"] = "没有确认"
            handover_list["hc_button"] = 1

        # 是否加冰判断
        if handover_list["gb_flag"] or handover_list["lb_flag"]:
            handover_list["is_ice"] = "是"
        else:
            handover_list["is_ice"] = "否"
        # 加冰种类判断
        handover_list["ice_type"] = ""
        if handover_list["gb_flag"]:
            handover_list["ice_type"] = handover_list["ice_type"] + "干冰"
        if handover_list["lb_flag"]:
            handover_list["ice_type"] = handover_list["ice_type"] + "蓝冰"
        # 加冰用量
        handover_list["ice_num"] = ""
        if handover_list["gb_flag"]:
            if not handover_list["gb_num"]:
                handover_list["gb_num"] = "0"
            handover_list["ice_num"] = handover_list["ice_num"] + "干冰," + handover_list["gb_num"]
        if handover_list["lb_flag"]:
            if not handover_list["lb_num"]:
                handover_list["lb_num"] = "0"
            if handover_list["ice_num"]:
                handover_list["ice_num"] = handover_list["ice_num"] + ";"
            handover_list["ice_num"] = handover_list["ice_num"] + "蓝冰," + handover_list["lb_num"]

        # TODO 判断展示button
        # TODO 三个文件位置

        return {
            "status": 200,
            "message": "获取电子交接单成功",
            "data": handover_list
        }

    def get_jc_pic(self):
        # TODO 入仓照片分批次，这个需要设计
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")

        jc_abo = {}
        jc_abo["jcno"] = args["jcno"]
        jc_abo["in"] = {}
        jc_abo["in"]["picture"] = []
        jc_abo["in"]["length"] = 0
        jc_abo["in"]["createtime"] = None
        jc_abo["in"]["czr"] = None
        jc_abo["out"] = {}
        jc_abo["out"]["picture"] = []
        jc_abo["out"]["length"] = 0
        jc_abo["out"]["createtime"] = None
        jc_abo["out"]["czr"] = None
        jc_abo["weight"] = {}
        jc_abo["weight"]["picture"] = []
        jc_abo["weight"]["length"] = 0
        jc_abo["weight"]["createtime"] = None
        jc_abo["weight"]["czr"] = None
        jc_abo["by"] = {}
        jc_abo["by"]["picture"] = []
        jc_abo["by"]["length"] = 0
        jc_abo["by"]["createtime"] = None
        jc_abo["by"]["czr"] = None
        make_log("jc_abo", jc_abo)
        if not jc_abo:
            return SYSTEM_ERROR
        quantity_weight = get_model_return_dict(self.sgoods.get_quantity_weight_by_jcno(args["jcno"]))
        if quantity_weight:

            jc_abo_in = get_model_return_list(self.sgoods.get_in_order_by_jcno(args["jcno"]))
            make_log("jc_abo_in", jc_abo_in)
            if jc_abo_in:
                for in_order in jc_abo_in:
                    jc_abo["in"]["picture"].append(in_order["photourl"])
                    jc_abo["in"]["createtime"] = in_order["createtime"].strftime("%Y-%m-%d %H:%M:%S")
                    # jc_abo["in"]["czr"] = in_order["czr"].decode("gbk").encode("utf8")
                    jc_abo["in"]["czr"] = in_order["czr"]
                jc_abo["in"]["length"] = len(jc_abo["in"]["picture"])
            jc_abo_out = get_model_return_list(self.sgoods.get_out_order_by_jcno(args["jcno"]))
            make_log("jc_abo_out", jc_abo_out)
            if jc_abo_out:
                for out_order in jc_abo_out:
                    jc_abo["out"]["picture"].append(out_order["photourl"])
                    jc_abo["out"]["createtime"] = out_order["createtime"].strftime("%Y-%m-%d %H:%M:%S")
                    # jc_abo["in"]["czr"] = in_order["czr"].decode("gbk").encode("utf8")
                    jc_abo["out"]["czr"] = out_order["czr"]
                jc_abo["out"]["length"] = len(jc_abo["out"]["picture"])
            jc_abo_weight = get_model_return_list(self.sgoods.get_weight_order_by_jcno(args["jcno"]))
            make_log("jc_abo_weight", jc_abo_weight)
            if jc_abo_weight:
                for weight_order in jc_abo_weight:
                    jc_abo["weight"]["picture"].append(weight_order["photourl"])
                    jc_abo["weight"]["createtime"] = weight_order["createtime"].strftime("%Y-%m-%d %H:%M:%S")
                    # jc_abo["in"]["czr"] = in_order["czr"].decode("gbk").encode("utf8")
                    jc_abo["weight"]["czr"] = weight_order["czr"]
                jc_abo["weight"]["length"] = len(jc_abo["weight"]["picture"])

            jc_abo_by = get_model_return_list(self.sgoods.get_by_order_by_jcno(args["jcno"]))
            make_log("jc_abo_by", jc_abo_by)
            if jc_abo_by:
                for by_order in jc_abo_by:
                    jc_abo["by"]["picture"].append(by_order["photourl"])
                    jc_abo["by"]["createtime"] = by_order["createtime"].strftime("%Y-%m-%d %H:%M:%S")
                    # jc_abo["in"]["czr"] = in_order["czr"].decode("gbk").encode("utf8")
                    jc_abo["by"]["czr"] = by_order["czr"]
                jc_abo["by"]["length"] = len(jc_abo["by"]["picture"])


        response = import_status("SUCCESS_GET_JC", "OK")
        response["data"] = jc_abo
        return response

    def get_jc_cb(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")

        qrd = get_model_return_list(self.sgoods.get_jc_qrd(args["jcno"]))
        print(qrd)
        jc_cb = {}
        jc_cb["jcno"] = None
        jc_cb["ydno"] = None
        jc_cb["company"] = None
        jc_cb["price"] = []
        if qrd:
            for row in qrd:
                price_dict = {}
                jc_cb["jcno"] = row["jcno"]
                jc_cb["ydno"] = row["ydno"]
                jc_cb["company"] = row["fkdw"]
                price_dict["curr"] = row["curr"]
                price_dict["amount"] = row["amount"]
                price_dict["doc"] = row["doc"]
                price_dict["id"] = row["id"]
                if row["byzd1"] == "1" and row["byzd3"] == "1":
                    price_dict["is_update"] = 1
                else:
                    price_dict["is_update"] = 0
                jc_cb["price"].append(price_dict)
        return {
            "status": 200,
            "message": "获取成本成功",
            "data": jc_cb
        }

    def get_fkdw(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ["fkdw"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        fkdw = get_model_return_list(self.sgoods.get_fkdw(args["fkdw"]))

        return {
            "status": 200,
            "message": "获取付款单位成功",
            "data": fkdw
        }

    def get_fyzl(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ["fyzl"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        fkdw = get_model_return_list(self.sgoods.get_fkzl(args["fyzl"]))

        return {
            "status": 200,
            "message": "获取费用种类成功",
            "data": fkdw
        }

    def get_in_abo(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")

        wts = get_model_return_dict(self.sgoods.get_ckmxd_wts(args["jcno"]))
        ckmxd = get_model_return_dict(self.sgoods.get_ckmxd_abo(args["jcno"]))
        if ckmxd:
            if ckmxd["enter_time"]:
                ckmxd["enter_time"] = ckmxd["enter_time"].strftime("%Y-%m-%d %H:%M:%S")
            wts.update(ckmxd)
        else:
            wts.update({
                "warehouse_address": None,
                "enter_time": None,
                "goods_quantity": None,
                "delivery_unit": None,
                "goods_weight": None,
                "cargo_size": None,
                "client_name": None,
                "remark": None
            })

        jc_abo_in = get_model_return_list(self.sgoods.get_in_order_by_jcno(args["jcno"]))
        make_log("jc_abo_in", jc_abo_in)
        wts["picture"] = []
        if jc_abo_in:
            for in_order in jc_abo_in:
                wts["picture"].append(in_order["photourl"])
                if wts["createtime"]:
                    wts["createtime"] = in_order["createtime"].strftime("%Y-%m-%d %H:%M:%S")
                wts["xsr"] = in_order["czr"]
        else:
            wts["createtime"] = None
            wts["xsr"] = None
        return {
            "status": 200,
            "message": "获取入库明细成功",
            "data": wts
        }

    def get_out_abo(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")

        wts = get_model_return_dict(self.sgoods.get_ckmxd_wts(args["jcno"]))
        if wts["ydno"]:
            outwarehouse = get_model_return_dict(self.sgoods.get_outwarehouse(wts["ydno"]))
            if outwarehouse:
                wts["is_button"] = 0
                if outwarehouse["submit_time"]:
                    outwarehouse["submit_time"] = outwarehouse["submit_time"].strftime("%Y/%m/%d %H:%M:%S")
                wts.update(outwarehouse)
            else:
                wts["is_button"] = 1
                wts.update({
                    "submitter": None,
                    "submit_time": None
                })
        else:
            wts["is_button"] = 1
            wts.update({
                "submitter": None,
                "submit_time": None
            })

        return {
            "status": 200,
            "message": "获取出库确认详情成功",
            "data": wts
        }

    def get_hc_abo(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")

        wts = get_model_return_dict(self.sgoods.get_ckmxd_wts(args["jcno"]))
        if wts["ydno"]:
            ingoodyard = get_model_return_dict(self.sgoods.get_ingoodyard(wts["ydno"]))
            if ingoodyard:
                wts["is_button"] = 0
                if ingoodyard["submit_time"]:
                    ingoodyard["submit_time"] = ingoodyard["submit_time"].strftime("%Y/%m/%d %H:%M:%S")
                wts.update(ingoodyard)
            else:
                wts["is_button"] = 1
                wts.update({
                    "submitter": None,
                    "submit_time": None
                })
        else:
            wts["is_button"] = 1
            wts.update({
                "submitter": None,
                "submit_time": None
            })

        return {
            "status": 200,
            "message": "获取出库确认详情成功",
            "data": wts
        }

    def get_sb_list(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")

        file_list = get_model_return_list(self.sgoods.get_sb_list(args["jcno"]))
        return {
            "status": 200,
            "message": "获取文件列表成功",
            "data": file_list
        }

    def get_bzsm_list(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")

        file_list = get_model_return_list(self.sgoods.get_bzsm_list(args["jcno"]))
        return {
            "status": 200,
            "message": "获取文件列表成功",
            "data": file_list
        }

    def get_jd_list(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")

        file_list = get_model_return_list(self.sgoods.get_jd_list(args["jcno"]))
        return {
            "status": 200,
            "message": "获取文件列表成功",
            "data": file_list
        }

    def get_sbno_list(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ["select_name", "page_size", "page_num"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        sbno_list = get_model_return_list(self.sgoods.get_sbno_list_like_ydno_jcno(args["select_name"],
                                                                                   int(args["page_size"]),
                                                                                   int(args["page_num"])))
        return {
            "status": 200,
            "message": "搜索成功",
            "data": sbno_list
        }

    def update_wts(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        data = json.loads(request.data)
        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")
        if "wts_type" not in data.keys():
            return {
                "status": 405,
                "status_code": 405001,
                "message": "参数缺失"
            }
        if data["wts_type"] == "jd":
            wts = get_model_return_dict(self.sgoods.get_id_by_jcno(args["jcno"]))
            wts_id = wts["id"]
            update_wts = self.sgoods.update_wts(wts_id, {
                "jd_time": datetime.datetime.now(),
                "ydno": wts["ydno"]
            })
            if not update_wts:
                return SYSTEM_ERROR
        return {
            "status": 200,
            "message": "交单成功"
        }

    def update_dzjjd(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        data = json.loads(request.data)
        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")
        if "dzjjd_type" not in data.keys():
            return {
                "status": 405,
                "status_code": 405001,
                "message": "参数缺失"
            }

        if data["dzjjd_type"] == "kfqr":
            dzjjd = get_model_return_dict(self.sgoods.get_jjdid_by_jcno(args["jcno"]))
            print(dzjjd)
            user = get_model_return_dict(self.susers.get_user_name(args["login_name"]))
            update_dzjjd = self.sgoods.update_dzjjd(dzjjd["jjd_id"], {
                "kf_ry": user["username"],
                "kfqr_date": datetime.datetime.now()
            })
            if not update_dzjjd:
                return SYSTEM_ERROR
        if data["dzjjd_type"] == "hcqr":
            dzjjd = get_model_return_dict(self.sgoods.get_jjdid_by_jcno(args["jcno"]))
            user = get_model_return_dict(self.susers.get_user_name(args["login_name"]))
            update_dzjjd = self.sgoods.update_dzjjd(dzjjd["jjd_id"], {
                "hc_ry": user["username"],
                "hcqr_date": datetime.datetime.now()
            })
            if not update_dzjjd:
                return SYSTEM_ERROR

        return {
            "status": 200,
            "message": str(data["dajjd_type"]) + "成功"
        }

    def upload_files(self):
        formdata = request.form
        make_log("formdata", formdata)
        files = request.files.get("file")

        import platform
        from Fansti.config import Inforcode
        if platform.system() == "Windows":
            rootdir = Inforcode.WindowsRoot + "/" + str(formdata.get("jcno"))
        else:
            rootdir = Inforcode.LinuxRoot + Inforcode.LinuxImgs
        print(rootdir)
        if not os.path.isdir(rootdir):
            os.mkdir(rootdir)
        rootdir = rootdir + "/" + str(formdata.get("FileType"))
        if not os.path.isdir(rootdir):
            os.mkdir(rootdir)
        if "FileType" not in formdata or "jcno" not in formdata:
            return {
                "status": 405,
                "status_code": 405001,
                "message": "参数缺失"
            }
        filessuffix = str(files.filename).split(".")[-1]
        index = formdata.get("index", 1)
        # filename = formdata.get("FileType") + str(index) + "." + filessuffix
        filename = formdata.get("FileType") + "_" + str(index) + "_" + str(uuid.uuid1()) + "." + filessuffix
        filepath = os.path.join(rootdir, filename)
        print(filepath)
        files.save(filepath)
        response = import_status("SUCCESS_MESSAGE_SAVE_FILE", "OK")
        url = Inforcode.ip + Inforcode.WindowsImag + "/" + str(formdata.get("jcno")) + "/" + str(formdata.get("FileType")) + "/" + filename
        print(url)
        response["data"] = url
        return response

    def add_in(self):
        # TODO 首次为写入，其余为更新
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())

        data = json.loads(request.data)
        make_log("data", data)

        wts = get_model_return_dict(self.sgoods.get_control_goods(args["jcno"]))
        # wts中获取jcno/czr/hwpm
        user = get_model_return_dict(self.susers.get_user_name(args["login_name"]))
        add_model("AIR_HWYS_CKMXD", **{
            "jcno": args["jcno"],
            "salesman": wts["czr"],
            "hwpm": data["hwpm"],
            "warehouse_address": data["warehouse_address"],
            "enter_time": datetime.datetime.strptime(data["enter_time"], "%Y-%m-%d %H:%M:%S"),
            "goods_quantity": data["goods_quantity"],
            "delivery_unit": data["delivery_unit"],
            "goods_weight": data["goods_weight"],
            "cargo_size": data["cargo_size"],
            "client_name": data["client_name"],
            "remark": data["remark"]
        })
        # TODO 分批次写入，方案未知
        for row in data["pic_list"]:
            add_model("AIR_HWYS_PHOTOS", **{
                "jcno": args["jcno"],
                "phototype": "入仓",
                "photourl": row["url"],
                "createtime": datetime.datetime.now(),
                "czr": user["user_name"],
                "filename": row["filename"]
            })
        return {
            "status": 200,
            "message": "提交成功"
        }

    def retrue_outhc(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        data = json.loads(request.data)
        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")
        if "retrue_type" not in data.keys():
            return {
                "status": 405,
                "status_code": 405001,
                "message": "参数缺失"
            }
        user = get_model_return_dict(self.susers.get_user_name(args["login_name"]))
        wts = get_model_return_dict(self.sgoods.get_control_goods(args["jcno"]))
        if data["retrue_type"] == "out":
            add_model("AIR_HWYS_OUTWAREHOUSE", **{
                "ydno": wts["ydno"],
                "submitter": user["user_name"],
                "submit_time": datetime.datetime.now(),
                "create_time": datetime.datetime.now()
            })
        if data["retrue_type"] == "hc":
            add_model("AIR_HWYS_INGOODYARD", **{
                "ydno": wts["ydno"],
                "submitter": user["user_name"],
                "submit_time": datetime.datetime.now(),
                "create_time": datetime.datetime.now()
            })

        return {
            "status": 200,
            "message": "确认成功"
        }

    def make_sb(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        data = json.loads(request.data)
        user = get_model_return_dict(self.susers.get_user_name(args["login_name"]))
        wts = get_model_return_dict(self.sgoods.get_control_goods(args["jcno"]))
        for row in data["jd_list"]:
            add_model("AIR_HWYS_DGD_UPLOAD", **{
                "jcno": args["jcno"],
                "ydno": wts["ydno"],
                "file_type": "鉴定文件",
                "file_url": row["url"],
                "create_time": datetime.datetime.now(),
                "create_user": user["username"],
                "file_name": row["file_name"]
            })
        for row in data["sb_list"]:
            add_model("AIR_HWYS_DGD_UPLOAD", **{
                "jcno": args["jcno"],
                "ydno": wts["ydno"],
                "file_type": "申报单",
                "file_url": row["url"],
                "create_time": datetime.datetime.now(),
                "create_user": user["username"],
                "file_name": row["file_name"]
            })
        for row in data["bzmx_list"]:
            add_model("AIR_HWYS_DGD_UPLOAD", **{
                "jcno": args["jcno"],
                "ydno": wts["ydno"],
                "file_type": "包装明细",
                "file_url": row["url"],
                "create_time": datetime.datetime.now(),
                "create_user": user["username"],
                "file_name": row["file_name"]
            })

        return {
            "status": 200,
            "message": "上传完毕"
        }

    def update_qrd(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno", "qrd_type"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        data = json.loads(request.data)
        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        user = get_model_return_dict(self.susers.get_user_name(args["login_name"]))
        wts = get_model_return_dict(self.sgoods.get_control_goods(args["jcno"]))
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")
        if args["qrd_type"] == "add":
            add_model("AIR_HWYS_QR", **{
                "ydno": wts["ydno"],
                "jcno": args["jcno"],
                "doc": data["doc"],
                "curr": data["curr"],
                "amount": data["amount"],
                "fkdw": data["fkdw"],
                "createtime": datetime.datetime.now(),
                "byzd2": user["username"]
            })
        if args["qrd_type"] == "update":
            update_qrd = self.sgoods.update_qrd_by_id(data["id"], {
                "ydno": wts["ydno"],
                "jcno": args["jcno"],
                "doc": data["doc"],
                "curr": data["curr"],
                "amount": data["amount"],
                "fkdw": data["fkdw"],
                "createtime": datetime.datetime.now(),
                "byzd2": user["username"]
            })
            if not update_qrd:
                return SYSTEM_ERROR

        if args["qrd_type"] == "delete":
            delete = self.sgoods.delete_qrd_by_id(data["id"])
            if not delete:
                return SYSTEM_ERROR
        return {
            "status": 200,
            "message": "编辑成功"
        }

    def get_packer(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ["select_name", "login_name"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        location = get_model_return_dict(self.susers.get_user_type(args["login_name"]))["location"]
        all_packer = get_model_return_list(self.susers.get_packer_by_select(args["select_name"], location))
        return {
            "status": 200,
            "message": "获取包装人员列表成功",
            "data": all_packer
        }

    def save_royalty(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        data = json.loads(request.data)
        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        user = get_model_return_dict(self.susers.get_user_name(args["login_name"]))
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")
        user_type_location = get_model_return_dict(self.susers.get_user_type(args["login_name"]))
        if user_type_location["user_type"] not in ["0", "3", "4"]:
            return {
                "status": 405,
                "status_code": 405999,
                "message": "无权限"
            }
        packer_leader = data["packer_leader"]
        for row in data["packer_list"]:
            add_model("AIR_HWYS_PACK_ROYALTY", **{
                "id": str(uuid.uuid1()),
                "jcno": args["jcno"],
                "packer_leader": packer_leader,
                "packer": row["packer"],
                "royalty_rate": None,
                "create_date": datetime.datetime.now(),
                "create_user": user["username"]
            })
        return {
            "status": 200,
            "message": "保存成功"
        }

    def update_royalty(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "jcno"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        data = json.loads(request.data)
        accounts = get_model_return_dict(self.sgoods.get_accounts_by_jcno(args["jcno"]))
        make_log("accounts", accounts)
        if args["login_name"] == accounts:
            return import_status("ERROR_NONE_PERMISSION", "FANSTI_ERROR", "ERROR_NONE_PERMISSION")
        if data["royalty_type"] == 0:
            royaltys = get_model_return_list(self.sgoods.get_royalty_by_jcno(args["jcno"]))
            for row in royaltys:
                update_response = self.sgoods.update_royalty(row["id"], {
                    "packer_confrim": "是"
                })
                if not update_response:
                    return SYSTEM_ERROR
        elif data["royalty_type"] == 1:
            royaltys = get_model_return_list(self.sgoods.get_royalty_by_jcno(args["jcno"]))
            for row in royaltys:
                update_response = self.sgoods.update_royalty(row["id"], {
                    "packer_ok": "是"
                })
                if not update_response:
                    return SYSTEM_ERROR
        return {
            "status": 200,
            "message": "更新成功"
        }