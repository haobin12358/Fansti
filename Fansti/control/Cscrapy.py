# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
from flask import request
from HTMLParser import HTMLParser
from Fansti.config.response import SYSTEM_ERROR, PARAMS_MISS
from Fansti.common.import_status import import_status
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.TransformToList import add_model
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list

class Cscrapy():
    def __init__(self):
        self.title = "=========={0}=========="
        from Fansti.services.Sscrapy import Sscrapy
        self.sscrapy = Sscrapy()

    def get_hs(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_keys = ["login_name", "hs_name"]
        if judge_keys(true_keys, args.keys()) != 200:
            return judge_keys(true_keys, args.keys())
        new_info = add_model("SELECT_INFO",
                             **{
                                 "id": str(uuid.uuid4()),
                                 "login_name": args["login_name"],
                                 "select_name": "HScode查询",
                                 "select_value": args["hs_name"]
                             })
        if not new_info:
            return SYSTEM_ERROR
        try:
            import urllib2
            url = "https://www.hsbianma.com/Code/{0}.html".format(args["code"])
            headers = {'Content-Type': 'application/xml'}
            req = urllib2.Request(url, headers=headers)
            url_response = urllib2.urlopen(req)
            strResult = url_response.read()
            parser = MyHTMLParser()
            parser.feed(strResult)
            length = len(parser.text)
            while length >= 0:
                print(parser.text[length - 1])
                if parser.text[length - 1].replace(" ", "") in ["\r\n", "\r\n\r\n", "\r\n\r\n\r\n", "]", "?"]:
                    parser.text.remove(parser.text[length - 1])
                length = length - 1
            data = [
                {
                    "name": "基本信息",
                    "value": []
                },
                {
                    "name": "所属章节",
                    "value": []
                },
                {
                    "name": "税率信息",
                    "value": []
                },
                {
                    "name": "申报要素",
                    "value": []
                },
                {
                    "name": "监管条件",
                    "value": []
                },
                {
                    "name": "检验检疫类别",
                    "value": []
                }
            ]
            first_key = ["基本信息", "所属章节", "税率信息", "申报要素", "监管条件", "检验检疫类别"]
            for row in parser.text:
                if row in first_key:
                    key_index = first_key.index(row)
                    row_index = parser.text.index(row)
                    while True:
                        print(self.title.format(""))
                        print parser.text[row_index + 1]
                        print parser.text[row_index + 2]
                        print(self.title.format(""))
                        a = {}
                        if parser.text[row_index + 1] in first_key or parser.text[row_index + 1] == "无" or parser.text[
                            row_index + 1] == "分享" or parser.text[row_index + 1] == "上一条:":
                            break
                        if parser.text[row_index + 1] == "CIQ代码(13位海关编码)" and parser.text[row_index + 2] == "编码状态":
                            a["name"] = parser.text[row_index + 1]
                            row_index = row_index + 1
                            a["value"] = ""
                        elif parser.text[row_index + 1] == "暂定税率" and parser.text[row_index + 2] == "进口普通税率":
                            a["name"] = parser.text[row_index + 1]
                            row_index = row_index + 1
                            a["value"] = ""
                        else:
                            a["name"] = parser.text[row_index + 1]
                            a["value"] = parser.text[row_index + 2].replace(" [", "")
                            row_index = row_index + 2
                        data[key_index]["value"].append(a)

            response = import_status("SUCCESS_GET_INFO", "OK")
            response["data"] = data
            return response
        except Exception as e:
            print e.message
            return SYSTEM_ERROR

    def get_cas(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_keys = ["login_name", "cas_name"]
        if judge_keys(true_keys, args.keys()) != 200:
            return judge_keys(true_keys, args.keys())
        new_info = add_model("SELECT_INFO",
                             **{
                                 "id": str(uuid.uuid4()),
                                 "login_name": args["login_name"],
                                 "select_name": "化工品信息查询",
                                 "select_value": args["cas_name"]
                             })
        if not new_info:
            return SYSTEM_ERROR
        try:
            import urllib2
            url = "http://www.ichemistry.cn/chemistry/{0}.htm".format(args["code"])
            headers = {'Content-Type': 'application/xml'}
            req = urllib2.Request(url, headers=headers)
            url_response = urllib2.urlopen(req)
            strResult = url_response.read()
            parser = MyHTMLParser()
            parser.feed(strResult)
            length = len(parser.text)
            while length >= 0:
                if parser.text[length - 1].replace(" ", "") in ["\r\n", "\r\n\r\n", "\r\n\r\n\r\n", "]", "?", "\r\n\t",
                                                                "\r\n\t\t", "\r\n\t\t\t", "\r\n\t\t\t\t'", ":"]:
                    parser.text.remove(parser.text[length - 1])
                elif "\r\n" in parser.text[length - 1] or "var" in parser.text[length - 1]:
                    parser.text.remove(parser.text[length - 1])
                length = length - 1
            print(parser.text)
            data = [
                {
                    "key": "基本信息",
                    "value": []
                },
                {
                    "key": "物理化学性质",
                    "value": []
                },
                {
                    "key": "安全信息",
                    "value": []
                },
                {
                    "key": "其他信息",
                    "value": []
                }
            ]
            keys = ["基本信息", "物理化学性质", "安全信息", "其他信息"]
            for row in parser.text:
                row_index = parser.text.index(row)
                if "基本信息" in row:
                    index = 0
                    item = {}
                    while True:
                        print(parser.text[row_index + index + 1])
                        if ":" in parser.text[row_index + index + 1] or parser.text[row_index + index + 1] == "CAS登录号":
                            if parser.text[row_index + index + 1] != parser.text[row_index + 1]:
                                data[0]["value"].append(item)
                                item = {}

                            item["name"] = parser.text[row_index + index + 1]
                            item["value"] = []
                        else:
                            if parser.text[row_index + index + 1] in "物理化学性质":
                                break
                            else:
                                item["value"].append(parser.text[row_index + index + 1])
                        index += 1

                elif row in keys:
                    key_index = keys.index(row)
                    index = 0
                    item = {}
                    while True:
                        print(parser.text[row_index + index + 1])
                        if ":" in parser.text[row_index + index + 1] or parser.text[row_index + index + 1] == "安全说明" \
                                or parser.text[row_index + index + 1] == "危险品标志" or parser.text[row_index + index + 1] == "危险类别码":
                            if parser.text[row_index + index + 1] != parser.text[row_index + 1]:
                                data[key_index]["value"].append(item)
                                item = {}

                            item["name"] = parser.text[row_index + index + 1]
                            item["value"] = []
                        else:
                            if parser.text[row_index + index + 1] in keys \
                                    or parser.text[row_index + index + 1] == "相关化学品信息":
                                break
                            else:
                                item["value"].append(parser.text[row_index + index + 1])
                        index += 1
            response = import_status("SUCCESS_GET_INFO", "OK")
            response["data"] = data
            return response
        except Exception as e:
            print e.message
            return SYSTEM_ERROR

    def get_jd(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_keys = ["login_name", "jd_name"]
        if judge_keys(true_keys, args.keys()) != 200:
            return judge_keys(true_keys, args.keys())
        new_info = add_model("SELECT_INFO",
                             **{
                                 "id": str(uuid.uuid4()),
                                 "login_name": args["login_name"],
                                 "select_name": "鉴定报告查询",
                                 "select_value": args["jd_name"]
                             })
        if not new_info:
            return SYSTEM_ERROR
        jd_report = get_model_return_dict(self.sscrapy.get_jd_by_name(args["jd_name"]))
        if not jd_report:
            return import_status("ERROR_FIND_JD", "FANSTI_ERROR", "ERROR_FIND_JD")
        for key in jd_report.keys():
            if not jd_report[key]:
                jd_report[key] = "暂无信息"
        data = [
            {
                "name": "中文品名",
                "value": jd_report["chinessname"]
            },
            {
                "name": "英文品名",
                "value": jd_report["englistname"]
            },
            {
                "name": "UN信息",
                "value": jd_report["unno"]
            },
            {
                "name": "颜色状态",
                "value": self.del_none(str(jd_report["appearance"]) + str(jd_report["appearance2"]))
            }
        ]
        response = import_status("SUCCESS_GET_INFO", "OK")
        response["data"] = data
        return response

    def del_none(self, str_word):
        str_word = str_word.replace("暂无信息", "")
        if not str_word:
            str_word = "暂无信息"
        return str_word

    def get_flyno(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_param = ["login_name"]
        if judge_keys(true_param, args.keys()) != 200:
            return judge_keys(true_param, args.keys())
        if "depa" not in args and "dest" not in args:
            return
        if "depa" not in args:
            args["depa"] = None
        if "dest" not in args:
            args["dest"] = None
        if not args["depa"]:
            if not args["dest"]:
                select_name = "0"
            else:
                select_name = "dest:" + str(args["dest"])
        else:
            if not args["dest"]:
                select_name = "depa:" + str(args["depa"])
            else:
                select_name = "depa:" + str(args["depa"]) + "dest:" + str(args["dest"])
        new_info = add_model("SELECT_INFO",
                             **{
                                 "id": str(uuid.uuid4()),
                                 "login_name": args["login_name"],
                                 "select_name": select_name,
                                 "select_value": args["jd_name"]
                             })
        if not new_info:
            return SYSTEM_ERROR
        all_airline = get_model_return_list(self.sscrapy.get_all_by_depa_dest(args["depa"], args["dest"]))
        make_log("all_airline", all_airline)
        if not all_airline:
            return SYSTEM_ERROR
        response = import_status("SUCCESS_GET_INFO", "OK")
        response["data"] = all_airline
        return response

    def new_update_airline(self):
        # TODO 上传格式规范的表格，如果格式不规范或者某行某列存在数据异常，提出报错
        # TODO 将文件存在linux存储在服务器中，最多储存30个文件，超过30个文件则清理掉，文件名称为时间.xls，例：20180729010101.xls
        # TODO 遍历表格，根据flight参数进行判断，如果数据库中存在，则更新，如果数据库中不存在，则增加一条数据
        pass


class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []

    def handle_data(self, data):
        self.text.append(data.decode("gbk").encode("utf8"))