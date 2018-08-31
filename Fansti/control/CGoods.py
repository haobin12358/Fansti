# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import json, uuid
from flask import request
from Fansti.config.response import SYSTEM_ERROR
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list
from Fansti.common.import_status import import_status
from Fansti.common.TransformToList import add_model

class CGoods():
    def __init__(self):
        from Fansti.services.SGoods import SGoods
        self.sgoods = SGoods()
        from Fansti.services.SUsers import SUsers
        self.susers = SUsers()

    def get_goods_list(self):
        args = request.args.to_dict()
        make_log("args", args)
        not_null_params = ['login_name', "page_size", "page_num"]
        if judge_keys(not_null_params, args.keys()) != 200:
            return judge_keys(not_null_params, args.keys())
        wts_filter = set()
        from Fansti.models.model import AIR_HWYS_WTS
        if args.get("ydno"):
            wts_filter.add(AIR_HWYS_WTS.ydno.like("%{0}%".format(args.get('ydno'))))
        if args.get("hxno"):
            wts_filter.add(AIR_HWYS_WTS.hxno.like("%{0}%".format(args.get("hxno"))))
        if args.get("destination"):
            wts_filter.add(AIR_HWYS_WTS.destination.like("%{0}%".format(args.get("destination"))))
            
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

        if usertype == 10:
            from sqlalchemy import or_
            wts_filter.add(or_(AIR_HWYS_WTS.czr == args.get("login_name"), AIR_HWYS_WTS.xsr == args.get("login_name")))
        elif usertype == 0:
            pass
        else:
            accounts = get_model_return_dict(self.susers.get_compnay_by_loginname(args["login_name"]))
            make_log("accounts", accounts)
            wts_filter.add(AIR_HWYS_WTS.accounts == accounts.get("compnay"))
        goods_list = get_model_return_list(self.sgoods.get_all_goods_by_filter(
            wts_filter, int(args["page_size"]), int(args["page_num"])))

        make_log("goods_list", goods_list)
        for goods in goods_list:
            yupei = get_model_return_dict(self.sgoods.get_dctime_by_jcno(goods["jcno"]))
            make_log("yupei", yupei)
            if not yupei:
                goods["yupei"] = "0"
            elif "hbdate1" in yupei.keys() and not yupei["hbdate1"]:
                goods["yupei"] = "0"
            else:
                goods["yupei"] = "1"
            jincang = get_model_return_list(self.sgoods.get_in_order_by_jcno(goods["jcno"]))
            make_log("jincang", jincang)
            #for row in jincang:
            if not jincang:
                goods["jincang"] = "0"
            else:
                goods["jincang"] = "1"
            chucang = get_model_return_list(self.sgoods.get_out_order_by_jcno(goods["jcno"]))
            make_log("chucang", chucang)
            #for row in chucang:
            if not chucang:
                goods["chucang"] = "0"
            else:
                goods["chucang"] = "1"
            chengzhong = get_model_return_list(self.sgoods.get_weight_order_by_jcno(goods["jcno"]))
            make_log("chengzhong", chengzhong)
            #for row in chengzhong:
            if not chengzhong:
                goods["chengzhong"] = "0"
            else:
                goods["chengzhong"] = "1"
            baoguan = get_model_return_dict(self.sgoods.get_content_by_jcno(goods["jcno"]))
            make_log("baoguan", baoguan)
            #for row in baoguan:
            if not baoguan:
                goods["baoguan"] = "0"
            elif "content" in baoguan.keys() and not baoguan["content"]:
                goods["baoguan"] = "0"
            else:
                goods['baoguan'] = "1"
            yundan = get_model_return_dict(self.sgoods.get_awb_by_jcno(goods["jcno"]))
            make_log("yundan", yundan)
            #for row in yundan:
            if not yundan:
                goods["yundan"] = "0"
            elif "content" in yundan.keys() and not yundan["content"]:
                goods["yundan"] = "0"
            else:
                goods["yundan"] = "1"
            jdtime = self.sgoods.get_jd_by_jcno(goods["jcno"])
            make_log("jiaodan", jdtime)
            jdtime = jdtime.jd_time or jdtime.jd_date
            if not jdtime:
                goods["jiaodan"] = "0"
            else:
                goods["jiaodan"] = "1"
            qifei = get_model_return_dict(self.sgoods.get_std(goods["jcno"]))
            make_log("qifei", qifei)
            if not qifei:
                goods["qifei"] = "0"
            elif "mes1" in qifei.keys() and not qifei["mes1"]:
                goods["qifei"] = "0"
            else:
                goods["qifei"] = "1"
            dida = get_model_return_dict(self.sgoods.get_dhmes_by_jcno(goods["jcno"]))
            make_log("dida", dida)
            if not dida:
                goods["dida"] = "0"
            elif "dhmes" in dida.keys() and not dida["dhmes"]:
                goods["dhmes"] = "0"
            else:
                goods["dida"] = "1"
            yanwu = get_model_return_list(self.sgoods.get_yanwu_by_jcno(goods["jcno"]))
            if not yanwu:
                goods["yanwu"] = "0"
            else:
                goods["yanwu"] = "1"
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
        if quantity_weight:
            jc_abo["quantity"] = quantity_weight["quantity"]
            jc_abo["weight"] = quantity_weight["weight"]
            jc_abo["in"] = {}
            jc_abo["in"]["picture"] = []
            jc_abo["out"] = {}
            jc_abo["out"]["picture"] = []
            jc_abo["weight_pic"] = {}
            jc_abo["weight_pic"]["picture"] = []
            jc_abo_in = get_model_return_list(self.sgoods.get_in_order_by_jcno(args["jcno"]))
            make_log("jc_abo_in", jc_abo_in)
            if jc_abo_in:
                for in_order in jc_abo_in:
                    jc_abo["in"]["createtime"] = in_order["createtime"].strftime("%Y-%m-%d %H:%M:%S")
                    # jc_abo["in"]["czr"] = in_order["czr"].decode("gbk").encode("utf8")
                    jc_abo["in"]["czr"] = in_order["czr"]
                    jc_abo["in"]["picture"].append(in_order["photourl"])
            jc_abo_out = get_model_return_list(self.sgoods.get_out_order_by_jcno(args["jcno"]))
            make_log("jc_abo_out", jc_abo_out)
            if jc_abo_out:
                for out_order in jc_abo_out:
                    jc_abo["out"]["createtime"] = out_order["createtime"].strftime("%Y-%m-%d %H:%M:%S")
                    # jc_abo["out"]["czr"] = out_order["czr"].decode("gbk").encode("utf8")
                    jc_abo["out"]["czr"] = out_order["czr"]
                    jc_abo["out"]["picture"].append(out_order["photourl"])
            jc_abo_weight = get_model_return_list(self.sgoods.get_weight_order_by_jcno(args["jcno"]))
            make_log("jc_abo_weight", jc_abo_weight)
            if jc_abo_weight:
                for weight_order in jc_abo_weight:
                    jc_abo["weight_pic"]["createtime"] = weight_order["createtime"].strftime("%Y-%m-%d %H:%M:%S")
                    # jc_abo["weight_pic"]["czr"] = weight_order["czr"].decode("gbk").encode("utf8")
                    jc_abo["weight_pic"]["czr"] = weight_order["czr"]
                    jc_abo["weight_pic"]["picture"].append(weight_order["photourl"])

            in_out_weight_status = get_model_return_list(self.sgoods.get_in_out_weight_by_jcno(args["jcno"]))
            jc_abo["in_status"] = "0"
            jc_abo["out_status"] = "0"
            jc_abo["weight_status"] = "0"
            for row in in_out_weight_status:
                if row["in_pic"] == "1":
                    jc_abo["in_status"] = "1"
                if row["out_pic"] == "1":
                    jc_abo["out_status"] = "1"
                if row["weight_pic"] == "1":
                    jc_abo["weight_status"] = "1"

        import datetime
        # 起飞
        jcno = args.get("jcno")
        make_log("jcno", jcno)
        jc_abo.update(get_model_return_dict(self.sgoods.get_std(jcno)))
        # 预配
        hbdate1 = get_model_return_dict(self.sgoods.get_dctime_by_jcno(jcno))
        make_log("hbdate1", hbdate1)
        if not hbdate1:
            jc_abo["hbdate1"] = None
        elif "hbdate1" in hbdate1.keys() and not hbdate1["hbdate1"]:
            jc_abo["hbdate1"] = None
        else:
            jc_abo["hbdate1"] = hbdate1["hbdate1"].strftime('%Y-%m-%d')
        # 交单
        jdtime = self.sgoods.get_jd_by_jcno(jcno)
        make_log("jdtime", jdtime)
        jdtime = jdtime.jd_time or jdtime.jd_date
        if not jdtime:
            jc_abo['supporttime'] = None
        else:
            jc_abo['supporttime'] = jdtime.strftime('%Y-%m-%d')

        # 送达
        jc_abo.update(get_model_return_dict(self.sgoods.get_dhmes_by_jcno(args.get("jcno"))))
        # 运单文件
        ydfile = get_model_return_list(self.sgoods.get_awbfile_by_jcno(args.get("jcno")))
        jc_abo['ydfile'] = ydfile
        # 报关单文件
        contentfile = get_model_return_list(self.sgoods.get_contentfile_by_jcno(args.get("jcno")))
        jc_abo['contentfile'] = contentfile
        response = import_status("SUCCESS_GET_JC", "OK")
        response["data"] = jc_abo
        return response

    def retrue_goods(self):
        args = request.args.to_dict()
        make_log("args", args)
        data = json.loads(request.data)
        make_log("data", data)
        true_args = ["login_name", "jcno"]
        true_data = ["retrue_name"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        if judge_keys(true_data, data.keys()) != 200:
            return judge_keys(true_data, data.keys())
        goods_retrue = get_model_return_list(self.sgoods.get_in_out_weight_by_jcno(args["jcno"]))
        if not goods_retrue:
            in_pic = "0"
            out_pic = "0"
            weight_pic = "0"
            if data["retrue_name"] == "in":
                in_pic = "1"
            if data["retrue_name"] == "out":
                out_pic = "1"
            if data["retrue_name"] == "weight":
                weight_pic = "1"
            new_goods_retrue = add_model("GOODS_RETRUE",
                                         **{
                                             "id": str(uuid.uuid4()),
                                             "login_name": args["login_name"],
                                             "in_pic": in_pic,
                                             "out_pic": out_pic,
                                             "weight_pic": weight_pic,
                                             "jcno": args["jcno"]
                                         })
            if not new_goods_retrue:
                return SYSTEM_ERROR
        else:
            if data["retrue_name"] == "in":
                id = get_model_return_dict(self.sgoods.get_retrue_by_jcno_in(args["jcno"]))
                if id:
                   return import_status("ERROR_FAIL_RETRUE", "FANSTI_ERROR", "ERROR_FAIL_RETRUE")
                else:
                    id_name = get_model_return_dict(self.sgoods.get_retrue_by_jcno_loginname(args["jcno"], args["login_name"]))
                    if not id_name:
                        new_goods_retrue = add_model("GOODS",
                                                     **{
                                                         "id": str(uuid.uuid4()),
                                                         "login_name": args["login_name"],
                                                         "in_pic": "1",
                                                         "out_pic": "0",
                                                         "weight_pic": "0",
                                                         "jcno": args["jcno"]
                                                     })
                        if not new_goods_retrue:
                            return SYSTEM_ERROR
                    else:
                        update_goods_retrue = self.sgoods.update_goods_retrue_by_id(id_name["id"], {"in_pic": "1"})
                        if not update_goods_retrue:
                            return SYSTEM_ERROR
            elif data["retrue_name"] == "out":
                id = get_model_return_dict(self.sgoods.get_retrue_by_jcno_out(args["jcno"]))
                if id:
                   return import_status("ERROR_FAIL_RETRUE", "FANSTI_ERROR", "ERROR_FAIL_RETRUE")
                else:
                    id_name = get_model_return_dict(self.sgoods.get_retrue_by_jcno_loginname(args["jcno"], args["login_name"]))
                    if not id_name:
                        new_goods_retrue = add_model("GOODS",
                                                     **{
                                                         "id": str(uuid.uuid4()),
                                                         "login_name": args["login_name"],
                                                         "in_pic": "0",
                                                         "out_pic": "1",
                                                         "weight_pic": "0",
                                                         "jcno": args["jcno"]
                                                     })
                        if not new_goods_retrue:
                            return SYSTEM_ERROR
                    else:
                        update_goods_retrue = self.sgoods.update_goods_retrue_by_id(id_name["id"], {"out_pic": "1"})
                        if not update_goods_retrue:
                            return SYSTEM_ERROR
            elif data["retrue_name"] == "weight":
                id = get_model_return_dict(self.sgoods.get_retrue_by_jcno_weight(args["jcno"]))
                if id:
                   return import_status("ERROR_FAIL_RETRUE", "FANSTI_ERROR", "ERROR_FAIL_RETRUE")
                else:
                    id_name = get_model_return_dict(self.sgoods.get_retrue_by_jcno_loginname(args["jcno"], args["login_name"]))
                    if not id_name:
                        new_goods_retrue = add_model("GOODS",
                                                     **{
                                                         "id": str(uuid.uuid4()),
                                                         "login_name": args["login_name"],
                                                         "in_pic": "0",
                                                         "out_pic": "0",
                                                         "weight_pic": "1",
                                                         "jcno": args["jcno"]
                                                     })
                        if not new_goods_retrue:
                            return SYSTEM_ERROR
                    else:
                        update_goods_retrue = self.sgoods.update_goods_retrue_by_id(id_name["id"], {"weight_pic": "1"})
                        if not update_goods_retrue:
                            return SYSTEM_ERROR
            else:
                return import_status("ERROR_WRONG_VALUE", "FANSTI_ERROR", "ERROR_WRONG_VALUE")
        # TODO 如果存在红包未领取，则修改红包状态
        return import_status("SUCCESS_RETRUE_GOODS", "OK")

    def get_retrue_num(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_args = ["login_name"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        if not args["login_name"]:
            retrue_num = 0
        all_retrue = get_model_return_list(self.sgoods.get_retrue_by_login_name(args["login_name"]))
        make_log("all_retrue", all_retrue)
        if not all_retrue:
            return SYSTEM_ERROR
        retrue_num = len(all_retrue)
        response = import_status("SUCCESS_GET_RETRUE", "OK")
        response["data"] = {}
        response["data"]["retrue_num"] = retrue_num
        return response
