# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import uuid, datetime, re, xlrd
from flask import request
from html.parser import HTMLParser
from Fansti.config.response import SYSTEM_ERROR, PARAMS_MISS
from Fansti.common.import_status import import_status
from Fansti.common.Log import make_log, judge_keys
from Fansti.common.TransformToList import add_model
from Fansti.common.get_model_return_list import get_model_return_dict, get_model_return_list
from Fansti.common.timeformate import get_db_time_str, format_forweb_no_second


class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []

    def handle_data(self, data):
        self.text.append(data)


class MyHTMLParser2(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []

    def handle_data(self, data):
        self.text.append(data)


class Cscrapy():
    def __init__(self):
        self.title = "=========={0}=========="
        from Fansti.services.Sscrapy import Sscrapy
        self.sscrapy = Sscrapy()

    def get_hs(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_keys = ["login_name", "hs_name", "openid"]
        if judge_keys(true_keys, args.keys()) != 200:
            return judge_keys(true_keys, args.keys())
        if args["login_name"] == "" and self.get_count("HScode", args["openid"]) >= 10:
            return import_status("ERROR_GET_SCRAPY", "FANSTI_ERROR", "ERROR_GET_SCRAPY")
        new_info = add_model("SELECT_INFO",
                             **{
                                 "id": str(uuid.uuid4()),
                                 "login_name": args["login_name"],
                                 "select_name": "HScode",
                                 "select_value": args["hs_name"],
                                 "openid": args["openid"],
                                 "create_time": str(datetime.datetime.now().date()).replace("-", "")
                             })
        if not new_info:
            return SYSTEM_ERROR
        try:
            import urllib.request
            url = "https://www.hsbianma.com/Code/{0}.html".format(args["hs_name"])
            req = urllib.request.urlopen(url)
            strResult = req.read()
            parser = MyHTMLParser2()
            parser.feed(strResult.decode(encoding="utf-8"))
            length = len(parser.text)

            while length >= 0:
                parser.text[length - 1] = parser.text[length - 1].replace(" ", "").replace("b\'", "").replace("\r", "").replace("\n", "").replace("[", "")
                if parser.text[length - 1] in ["b\'\r\n ", "\\r\\n\\r\\n", "\\r\\n\\r\\n\\r\\n", "]", "?", ""]:
                    parser.text.remove(parser.text[length - 1])
                length = length - 1
            print(parser.text)
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
                print(row.encode("utf8"))
                if row in first_key:
                    key_index = first_key.index(row)
                    row_index = parser.text.index(row)
                    while True:
                        print(self.title.format(""))
                        print(parser.text[row_index + 1])
                        print(parser.text[row_index + 2])
                        print(self.title.format(""))
                        a = {}
                        if parser.text[row_index + 1] in first_key or parser.text[row_index + 1].encode("utf8") == "无" or parser.text[
                            row_index + 1] == "分享" or parser.text[row_index + 1] == "上一条:":
                            break
                        if parser.text[row_index + 1].encode("utf8") == "CIQ代码(13位海关编码)" and parser.text[row_index + 2].encode("utf8") == "编码状态":
                            a["name"] = parser.text[row_index + 1]
                            row_index = row_index + 1
                            a["value"] = ""
                        elif parser.text[row_index + 1].encode("utf8") == "暂定税率" and parser.text[row_index + 2].encode("utf8") == "进口普通税率":
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
            print(e)
            return SYSTEM_ERROR

    def get_cas(self):
        try:
            args = request.args.to_dict()
            make_log("args", args)
            true_keys = ["login_name", "cas_name", "openid"]
            if judge_keys(true_keys, args.keys()) != 200:
                return judge_keys(true_keys, args.keys())
            if args["login_name"] == "" and self.get_count("cas", args["openid"]) >= 10:
                return import_status("ERROR_GET_SCRAPY", "FANSTI_ERROR", "ERROR_GET_SCRAPY")
            new_info = add_model("SELECT_INFO",
                                 **{
                                     "id": str(uuid.uuid4()),
                                     "login_name": args["login_name"],
                                     "select_name": "cas",
                                     "select_value": args["cas_name"],
                                     "openid": args["openid"],
                                     "create_time": str(datetime.datetime.now().date()).replace("-", "")
                                 })
            if not new_info:
                return SYSTEM_ERROR
            import urllib.request
            url = "http://www.ichemistry.cn/chemistry/{0}.htm".format(args["cas_name"])
            headers = {'Content-Type': 'application/xml'}
            req = urllib.request.urlopen(url)
            strResult = req.read()
            parser = MyHTMLParser()
            parser.feed(strResult.decode('gbk','ignore'))
            length = len(parser.text)
            while length >= 0:
                parser.text[length - 1] = parser.text[length - 1].replace(" ", "").replace("\t", "").replace("\r","").replace("\n", "")
                if parser.text[length - 1].replace(" ", "") in ["\r\n", "\r\n\r\n", "\r\n\r\n\r\n", "]", "?", "\r\n\t",
                                                                "\r\n\t\t", "\r\n\t\t\t", "\r\n\t\t\t\t'", ":", ""]:
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
            print(e)
            return SYSTEM_ERROR

    def get_jd(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_keys = ["login_name", "jd_name", "openid"]
        if judge_keys(true_keys, args.keys()) != 200:
            return judge_keys(true_keys, args.keys())
        if args["login_name"] == "" and self.get_count("jd", args["openid"]) >= 10:
            return import_status("ERROR_GET_SCRAPY", "FANSTI_ERROR", "ERROR_GET_SCRAPY")
        new_info = add_model("SELECT_INFO",
                             **{
                                 "id": str(uuid.uuid4()),
                                 "login_name": args["login_name"],
                                 "select_name": "jd",
                                 "select_value": args["jd_name"],
                                 "openid": args["openid"],
                                 "create_time": str(datetime.datetime.now().date()).replace("-", "")
                             })
        if not new_info:
            return SYSTEM_ERROR
        jd_report = get_model_return_dict(self.sscrapy.get_jd_by_name(args["jd_name"]))
        make_log("jd_report", jd_report)
        if not jd_report:
            return import_status("ERROR_FIND_JD", "FANSTI_ERROR", "ERROR_FIND_JD")
        for key in jd_report.keys():
            if not jd_report[key]:
                if key != "appearance" and key != "appearance2":
                    jd_report[key] = "暂无信息"
        if not jd_report["appearance"]:
            if not jd_report["appearance2"]:
                appearance = "暂无信息"
            else:
                appearance = jd_report["appearance2"]
        else:
            if not jd_report["appearance2"]:
                appearance = jd_report["appearance"]
            else:
                appearance = jd_report["appearance"] \
                             + jd_report["appearance2"]
        data = [
            {
                "name": "中文品名",
                "value": self.make_code(jd_report["chinesename"])
            },
            {
                "name": "英文品名",
                "value": jd_report["englishname"]
            },
            {
                "name": "UN信息",
                "value": self.make_code(jd_report["unno"])
            },
            {
                "name": "颜色状态",
                "value": appearance
            }
        ]
        response = import_status("SUCCESS_GET_INFO", "OK")
        response["data"] = data
        return response

    def get_flyno(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_param = ["login_name", "openid"]
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
        if args["login_name"] == "" and self.get_count("flyno", args["openid"]) >= 10:
            return import_status("ERROR_GET_SCRAPY", "FANSTI_ERROR", "ERROR_GET_SCRAPY")
        new_info = add_model("SELECT_INFO",
                             **{
                                 "id": str(uuid.uuid4()),
                                 "login_name": args["login_name"],
                                 "select_name": "flyno",
                                 "select_value": select_name,
                                 "openid": args["openid"],
                                 "create_time": str(datetime.datetime.now().date()).replace("-", "")
                             })
        if not new_info:
            return SYSTEM_ERROR
        all_airline = get_model_return_list(self.sscrapy.get_all_by_depa_dest(args["depa"], args["dest"]))
        make_log("all_airline", all_airline)
        for airline in all_airline:
            airline["mydate"] = datetime.datetime.strptime(airline["mydate"], '%Y-%m-%d').strftime("%Y-%m-%d")
            airline["etd"] = airline["etd"].strftime("%Y-%m-%d %H:%M")
            airline["eta"] = airline["eta"].strftime("%Y-%m-%d %H:%M")
        if not all_airline:
            return SYSTEM_ERROR
        response = import_status("SUCCESS_GET_INFO", "OK")
        response["data"] = all_airline
        return response

    def new_update_airline(self):
        # 上传格式规范的表格，如果格式不规范或者某行某列存在数据异常，提出报错
        # 将文件存在linux存储在服务器中，最多储存10天文件（默认），超过10天的文件则清理掉，文件名称为时间.xls，例：20180729010101.xls
        # 遍历表格，根据flight参数进行判断，如果数据库中存在，则更新，如果数据库中不存在，则增加一条数据
        # D:\teamsystem\Fansti
        filepath = self.save_file("AIRLINE")
        if not isinstance(filepath, str):
            return filepath
        # titlekey = ['AIRLINE', 'NAME', 'COMPANY', 'FLIGHT', 'DEPA', 'DEST',
        #             'DATE', 'ETD', 'ETA', '交单时间', 'AIRCRAFT', 'REMARK']

        wb = xlrd.open_workbook(filepath)
        sheet1 = wb.sheet_by_index(0)
        title_line = sheet1.row_values(0)
        title_line = [title.encode("utf8") if False else title for title in title_line]
        make_log("title_line", title_line)
        keydict = {k: v for v, k in enumerate(title_line)}
        make_log("keydict", keydict)
        from Fansti.config.staticconfig import AIRLINE_DB_TO_EXCEL, AIRLINE_EXCEL_ROLE
        keyindex_to_db = {key: keydict.get(AIRLINE_DB_TO_EXCEL.get(key)) for key in AIRLINE_DB_TO_EXCEL}

        make_log("keyindex_to_db", keyindex_to_db)

        make_log("sheet1.nrows", sheet1.nrows)
        airline = ""
        airname = ""
        aipcompany = ""
        depa = ""
        dest = ""
        remark = ""
        for row in range(1, sheet1.nrows):
            row_data = sheet1.row_values(row, 0)
            row_dict = {
                k: row_data[keyindex_to_db.get(k)] for k in keyindex_to_db
            }

            # 合并单元格处理
            if row_dict.get("airline"):
                airline = row_dict.get("airline")
            else:
                row_dict["airline"] = airline

            if row_dict.get("airname"):
                airname = row_dict.get("airname")
            else:
                row_dict["airname"] = airname

            if row_dict.get("aircompany"):
                aipcompany = row_dict.get("aircompany")

            else:
                row_dict["aircompany"] = aipcompany

            if row_dict.get("depa"):
                depa = row_dict.get("depa")
            else:
                row_dict["depa"] = depa

            if row_dict.get("dest"):
                dest = row_dict.get("dest")
            else:
                row_dict["dest"] = dest

            if row_dict.get("remark"):
                remark = row_dict.get("remark")
            else:
                row_dict["remark"] = remark

            for key in row_dict:

                # 正则校验
                try:
                    if AIRLINE_EXCEL_ROLE.get(key) and row_dict.get(key) and not re.match(AIRLINE_EXCEL_ROLE.get(key), row_dict.get(key)):
                        response = import_status("ERROR_FAIL_FILE", "FANSTI_ERROR", "ERROR_FAIL_FILE")
                        response["data"] = {
                            "row": row,
                            "col": key
                        }
                        return response
                except Exception as e:
                    print(e)
                    print(AIRLINE_EXCEL_ROLE.get(key))
                    print(key)
                    print(row_dict.get(key))

            make_log("row_dict", row_dict)
            # eta etd date 修改
            eta_list = row_dict.get("eta").split("+")
            eta_data = row_dict.get("mydate") + " " + eta_list[0]
            eta_data = datetime.datetime.strptime(eta_data, format_forweb_no_second)

            if len(eta_list) > 1 and eta_list[1]:
                if re.match(r"\d+", eta_list[1]):
                    eta_data = eta_data + datetime.timedelta(days=int(eta_list[1]))

            etd_list = row_dict.get("etd").split("+")
            etd_date = row_dict.get("mydate") + " " + etd_list[0]
            etd_date = datetime.datetime.strptime(etd_date, format_forweb_no_second)

            row_dict["eta"] = eta_data
            row_dict["etd"] = etd_date

            airhwysline = self.sscrapy.get_airline_by_flight(row_dict.get("flight"))
            if airhwysline:
                update_result = self.sscrapy.update_airline(row_dict.get("flight"), row_dict)
                if not update_result:
                    response = import_status("ERROR_FAIL_FILE", "FANSTI_ERROR", "ERROR_FAIL_FILE")
                    response["data"] = row
                    return response
            else:
                row_dict["id"] = str(uuid.uuid1())
                self.sscrapy.add_model("AIR_HWYS_LINES", **row_dict)

        response = import_status("SUCCESS_MESSAGE_SAVE_FILE", "OK")
        return response

    def get_all_scrapy(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_params = ["page_size", "page_num", "select_name"]
        if judge_keys(true_params, args.keys()) != 200:
            return judge_keys(true_params, args.keys())
        all_select = get_model_return_list(self.sscrapy.get_all_select(int(args["page_num"]), int(args["page_size"])
                                                                       , args["select_name"]))
        make_log("all_select", all_select)
        count = len(all_select)
        response = import_status("SUCCESS_GET_RETRUE", "OK")
        response["data"] = {}
        response["data"]["all_select"] = all_select
        response["data"]["count"] = count

        return response

    def get_dgr(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_keys = ["login_name", "dgr_name", "openid"]
        if judge_keys(true_keys, args.keys()) != 200:
            return judge_keys(true_keys, args.keys())
        if args["login_name"] == "" and self.get_count("dgr", args["openid"]) >= 10:
            return import_status("ERROR_GET_SCRAPY", "FANSTI_ERROR", "ERROR_GET_SCRAPY")
        new_info = add_model("SELECT_INFO",
                             **{
                                 "id": str(uuid.uuid4()),
                                 "login_name": args["login_name"],
                                 "select_name": "dgr",
                                 "select_value": args["dgr_name"],
                                 "openid": args["openid"],
                                 "create_time": str(datetime.datetime.now().date()).replace("-", "")
                             })
        if not new_info:
            return SYSTEM_ERROR
        dgr = get_model_return_dict(self.sscrapy.get_dgr_by_unno(args["dgr_name"]))
        make_log("dgr", dgr)
        if not dgr:
            return SYSTEM_ERROR
        dgr_type = get_model_return_list(self.sscrapy.get_dgr_level_by_dgrid(dgr["id"]))
        make_log("dgr_type", dgr_type)
        if not dgr:
            return SYSTEM_ERROR
        for row in dgr_type:
            row["airliner_is_single"] = self.make_code(row["airliner_is_single"])
            row["airfreighter_is_single"] = self.make_code(row["airfreighter_is_single"])
            dgr_con = get_model_return_list(self.sscrapy.get_dgr_container_by_levelid(row["id"]))
            for raw in dgr_con:
                raw["dgr_container"] = raw["dgr_container"]
                raw["dgr_type"] = raw["dgr_type"]
            if not dgr_con:
                return
            row["dgr_con"] = dgr_con
        dgr["dgr_type"] = dgr_type

        response = import_status("SUCCESS_GET_RETRUE", "OK")
        response["data"] = dgr
        return response

    def get_tact(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_keys = ["login_name", "tact_name", "openid"]
        if judge_keys(true_keys, args.keys()) != 200:
            return judge_keys(true_keys, args.keys())
        if args["login_name"] == "" and self.get_count("tact", args["openid"]) >= 10:
            return import_status("ERROR_GET_SCRAPY", "FANSTI_ERROR", "ERROR_GET_SCRAPY")
        new_info = add_model("SELECT_INFO",
                             **{
                                 "id": str(uuid.uuid4()),
                                 "login_name": args["login_name"],
                                 "select_name": "tact",
                                 "select_value": args["tact_name"],
                                 "openid": args["openid"],
                                 "create_time": str(datetime.datetime.now().date()).replace("-", "")
                             })
        if not new_info:
            return SYSTEM_ERROR

        tact = get_model_return_dict(self.sscrapy.get_tact_by_three_code(args["tact_name"]))
        make_log("tact", tact)
        if not tact:
            return SYSTEM_ERROR
        tact["chinese_position"] = self.make_code(tact["chinese_position"])

        response = import_status("SUCCESS_GET_RETRUE", "OK")
        response["data"] = tact
        return response

    def get_count(self, select_name, openid):
        date = str(datetime.datetime.now().date()).replace("-", "")
        count = len(get_model_return_list(self.sscrapy.get_id_by_time(date, select_name, openid)))
        return count

    def make_code(self, str_word):
        try:
            str_word = str_word.decode("gbk").encode("utf8")
        except:
            str_word = str(str_word)
        return str_word

    def upload_template_dgr(self):
        filepath = self.save_file("DGR")
        if not isinstance(filepath, str):
            return filepath

        wb = xlrd.open_workbook(filepath)
        sheet1 = wb.sheet_by_index(0)
        title_line = sheet1.row_values(0)
        title_line = [title.encode("utf8") if isinstance(title, unicode) else title for title in title_line]
        make_log("title_line", title_line)
        from Fansti.config.staticconfig import DGR_DB_TO_EXCEL, CONTAINER_KEY,\
            DGR_KEY, DGR_LEVEL_KEY, DGR_LEVEL_DB_TO_EXCEL
        dgr_key_dict = {k: v for v, k in enumerate(title_line) if k in DGR_KEY}
        dgr_level_dict = {k: v for v, k in enumerate(title_line) if k in DGR_LEVEL_KEY}
        dgr_container_dict = {k: v for v, k in enumerate(title_line) if k in CONTAINER_KEY}
        # check title key
        for key in CONTAINER_KEY + DGR_LEVEL_KEY + DGR_KEY:
            if key not in title_line:
                response = import_status("ERROR_FAIL_FILE", "FANSTI_ERROR", "ERROR_FAIL_FILE")
                response['data'] = {
                    "row": 0,
                    "key": key,
                    "reason": "the title is not right need {0} necessary".format(key)
                }
                return response

        make_log("dgr_key_dict", dgr_key_dict)
        make_log("dgr_level_dict", dgr_level_dict)
        make_log("dgr_container_dict", dgr_container_dict)

        dgr_key_index_to_db = {key: dgr_key_dict.get(DGR_DB_TO_EXCEL.get(key)) for key in DGR_DB_TO_EXCEL}
        dgr_level_index_to_db = {
            key: dgr_level_dict.get(DGR_LEVEL_DB_TO_EXCEL.get(key)) for key in DGR_LEVEL_DB_TO_EXCEL}

        make_log("dgr_key_index_to_db", dgr_key_index_to_db)
        make_log("dgr_level_index_to_db", dgr_level_index_to_db)

        make_log("sheet1.nrows", sheet1.nrows)

        # init
        dgrid = str(uuid.uuid1())
        dgrlevelid = str(uuid.uuid1())

        for dgr_row in range(1, sheet1.nrows):
            dgr_row_value = sheet1.row_values(dgr_row)

            # dgr model
            if dgr_row_value[dgr_key_index_to_db.get("unno")]:
                dgrid = str(uuid.uuid1())
                dgr_model_dict = {
                    "id": dgrid,
                    "unno": dgr_row_value[dgr_key_index_to_db.get("unno")],
                    "unname": dgr_row_value[dgr_key_index_to_db.get("unname")],
                    "untype": dgr_row_value[dgr_key_index_to_db.get("untype")],
                }
                # 内容格式编码处理以及去空格处理+ TODO 正则校验
                for key in dgr_model_dict:
                    # 空格处理
                    if isinstance(dgr_model_dict.get(key), unicode):
                        dgr_model_dict[key] = re.sub(r"[\n\t\s]", "", dgr_model_dict.get(key))

                    # # 正则校验
                    # try:
                    #     if AIRLINE_EXCEL_ROLE.get(key) and row_dict.get(key) and not re.match(
                    #             AIRLINE_EXCEL_ROLE.get(key), row_dict.get(key)):
                    #         response = import_status("ERROR_FAIL_FILE", "FANSTI_ERROR", "ERROR_FAIL_FILE")
                    #         response["data"] = {
                    #             "row": row,
                    #             "col": key
                    #         }
                    #         return response
                    # except Exception as e:
                    #     print(e.message)
                    #     print(AIRLINE_EXCEL_ROLE.get(key))
                    #     print(key)
                    #     print row_dict.get(key)
                    # 字符编码处理
                    if isinstance(dgr_model_dict.get(key), unicode):
                        dgr_model_dict[key] = dgr_model_dict.get(key).encode("utf8")

                make_log("dgr_model_dict", dgr_model_dict)
                self.sscrapy.add_model("AIR_HWYS_DGR", **dgr_model_dict)

            # dgr level model
            if dgr_row_value[dgr_level_index_to_db.get("dgr_level")]:
                dgrlevelid = str(uuid.uuid1())
                dgr_level_model_dict = {
                    "id": dgrlevelid,
                    "dgr_id": dgrid,
                    "dgr_level": dgr_row_value[dgr_level_index_to_db.get("dgr_level")],
                    "airliner_capacity": dgr_row_value[dgr_level_index_to_db.get("airliner_capacity")],
                    "airliner_description_no": dgr_row_value[dgr_level_index_to_db.get("airliner_description_no")],
                    "airliner_is_single": dgr_row_value[dgr_level_index_to_db.get("airliner_is_single")],
                    "airfreighter_capacity": dgr_row_value[dgr_level_index_to_db.get("airfreighter_capacity")],
                    "airfreighter_description_no": dgr_row_value[dgr_level_index_to_db.get("airfreighter_description_no")],
                    "airfreighter_is_single": dgr_row_value[dgr_level_index_to_db.get("airfreighter_is_single")],
                    "message": dgr_row_value[dgr_level_index_to_db.get("message")],
                }

                # 内容格式编码处理以及去空格处理+ TODO 正则校验
                for key in dgr_level_model_dict:
                    # 空格处理
                    if isinstance(dgr_level_model_dict.get(key), unicode):
                        dgr_level_model_dict[key] = re.sub(r"[\n\t\s]", "", dgr_level_model_dict.get(key))

                    # # 正则校验
                    # try:
                    #     if AIRLINE_EXCEL_ROLE.get(key) and row_dict.get(key) and not re.match(
                    #             AIRLINE_EXCEL_ROLE.get(key), row_dict.get(key)):
                    #         response = import_status("ERROR_FAIL_FILE", "FANSTI_ERROR", "ERROR_FAIL_FILE")
                    #         response["data"] = {
                    #             "row": row,
                    #             "col": key
                    #         }
                    #         return response
                    # except Exception as e:
                    #     print(e.message)
                    #     print(AIRLINE_EXCEL_ROLE.get(key))
                    #     print(key)
                    #     print row_dict.get(key)
                    # 字符编码处理
                    if isinstance(dgr_level_model_dict.get(key), unicode):
                        dgr_level_model_dict[key] = dgr_level_model_dict.get(key).encode("utf8")

                make_log("dgr_level_model_dict", dgr_level_model_dict)
                self.sscrapy.add_model("AIR_HWYS_DGR_LEVEL", **dgr_level_model_dict)

            # dgr container model
            if dgr_row_value[dgr_container_dict.get("客机容器类型")]:
                airliner_container_dict = {
                    "id": str(uuid.uuid1()),
                    "dgr_level_id": dgrlevelid,
                    "dgr_container": dgr_row_value[dgr_container_dict.get("客机容器类型")],
                    "dgr_container_capacity": dgr_row_value[dgr_container_dict.get("客机容器类型对应容量")],
                    "dgr_type": "客机",
                }

                # 内容格式编码处理以及去空格处理+ TODO 正则校验
                for key in airliner_container_dict:
                    # 空格处理
                    if isinstance(airliner_container_dict.get(key), unicode):
                        airliner_container_dict[key] = re.sub(r"[\n\t\s]", "", airliner_container_dict.get(key))

                    # # 正则校验
                    # try:
                    #     if AIRLINE_EXCEL_ROLE.get(key) and row_dict.get(key) and not re.match(
                    #             AIRLINE_EXCEL_ROLE.get(key), row_dict.get(key)):
                    #         response = import_status("ERROR_FAIL_FILE", "FANSTI_ERROR", "ERROR_FAIL_FILE")
                    #         response["data"] = {
                    #             "row": row,
                    #             "col": key
                    #         }
                    #         return response
                    # except Exception as e:
                    #     print(e.message)
                    #     print(AIRLINE_EXCEL_ROLE.get(key))
                    #     print(key)
                    #     print row_dict.get(key)
                    # 字符编码处理
                    if isinstance(airliner_container_dict.get(key), unicode):
                        airliner_container_dict[key] = airliner_container_dict.get(key).encode("utf8")
                make_log("airliner_container_dict", airliner_container_dict)
                self.sscrapy.add_model("AIR_HWYS_DGR_CONTAINER", **airliner_container_dict)

            if dgr_row_value[dgr_container_dict.get("货机容器类型")]:
                airfreighter_container_dict = {
                    "id": str(uuid.uuid1()),
                    "dgr_level_id": dgrlevelid,
                    "dgr_container": dgr_row_value[dgr_container_dict.get("货机容器类型")],
                    "dgr_container_capacity": dgr_row_value[dgr_container_dict.get("货机容器类型对应容量")],
                    "dgr_type": "客机",
                }

                # 内容格式编码处理以及去空格处理+ TODO 正则校验
                for key in airfreighter_container_dict:
                    # 空格处理
                    if isinstance(airfreighter_container_dict.get(key), unicode):
                        airfreighter_container_dict[key] = re.sub(r"[\n\t\s]", "", airfreighter_container_dict.get(key))

                    # # 正则校验
                    # try:
                    #     if AIRLINE_EXCEL_ROLE.get(key) and row_dict.get(key) and not re.match(
                    #             AIRLINE_EXCEL_ROLE.get(key), row_dict.get(key)):
                    #         response = import_status("ERROR_FAIL_FILE", "FANSTI_ERROR", "ERROR_FAIL_FILE")
                    #         response["data"] = {
                    #             "row": row,
                    #             "col": key
                    #         }
                    #         return response
                    # except Exception as e:
                    #     print(e.message)
                    #     print(AIRLINE_EXCEL_ROLE.get(key))
                    #     print(key)
                    #     print row_dict.get(key)
                    # 字符编码处理
                    if isinstance(airfreighter_container_dict.get(key), unicode):
                        airfreighter_container_dict[key] = airfreighter_container_dict.get(key).encode("utf8")
                make_log("airfreighter_container_dict", airfreighter_container_dict)
                self.sscrapy.add_model("AIR_HWYS_DGR_CONTAINER", **airfreighter_container_dict)


        response = import_status("ERROR_FAIL_FILE", "FANSTI_ERROR", "ERROR_FAIL_FILE")
        return response

    def save_file(self, file_type):
        formdata = request.form
        make_log("formdata", formdata)
        files = request.files.get("file")
        import platform
        from Fansti.config import Inforcode

        file_dir = Inforcode.template_type_dir.get(file_type)

        if platform.system() == "Windows":
            rootdir = os.path.join(Inforcode.WindowsRoot, file_dir)
        else:
            rootdir = os.path.join(Inforcode.LinuxTMP, file_dir)
        if not os.path.isdir(rootdir):
            os.mkdir(rootdir)
        # if "FileType" not in formdata:
        #     return
        filessuffix = str(files.filename).split(".")[-1]
        if filessuffix not in ["xls", "xlsm", "xlsx"]:
            return import_status("ERROR_FAIL_TYPE", "FANSTI_ERROR", "ERROR_FAIL_TYPE")

        filename = get_db_time_str() + "." + filessuffix
        filepath = os.path.join(rootdir, filename)
        print(filepath)
        files.save(filepath)
        return filepath
