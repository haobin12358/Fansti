# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
from HTMLParser import HTMLParser
from Fansti.config.response import SYSTEM_ERROR, PARAMS_MISS

class Cscrapy():
    def __init__(self):
        self.title = "=========={0}=========="

    def get_hs(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args or "code" not in args:
            return PARAMS_MISS
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
            print length
            while length >= 0:
                print(parser.text[length - 1])
                if parser.text[length - 1].replace(" ", "") in ["\r\n", "\r\n\r\n", "\r\n\r\n\r\n", "]", "?"]:
                    parser.text.remove(parser.text[length - 1])
                length = length - 1
            print(parser.text)
            print(len(parser.text))
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

            return data
        except Exception as e:
            print 1
            print e.message

    def get_cas(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args or "code" not in args:
            return PARAMS_MISS
        try:
            import urllib2
            url = "http://www.ichemistry.cn/chemistry/{0}.htm".format(args["code"])
            headers = {'Content-Type': 'application/xml'}
            req = urllib2.Request(url, headers=headers)
            url_response = urllib2.urlopen(req)
            strResult = url_response.read()
            parser = MyHTMLParser()
            parser.feed(strResult)
            # print(parser.text)
            length = len(parser.text)
            # print length
            while length >= 0:
                if parser.text[length - 1].replace(" ", "") in ["\r\n", "\r\n\r\n", "\r\n\r\n\r\n", "]", "?", "\r\n\t",
                                                                "\r\n\t\t", "\r\n\t\t\t", "\r\n\t\t\t\t'", ":"]:
                    parser.text.remove(parser.text[length - 1])
                elif "\r\n" in parser.text[length - 1] or "var" in parser.text[length - 1]:
                    parser.text.remove(parser.text[length - 1])
                length = length - 1
            print(parser.text)
            # print(len(parser.text))
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
                # a = row.decode("gbk")
                # print row
                if "基本信息" in row:
                    index = 0
                    item = {}
                    # item["value"] = []
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
                # print(row.decode("gbk"))
            return data
        except Exception as e:
            print 1
            print e.message

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []

    def handle_data(self, data):
        self.text.append(data.decode("gbk").encode("utf8"))