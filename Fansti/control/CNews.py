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
        true_args = ["page_size", "page_num"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
        all_news = get_model_return_list(self.snews.get_all(int(args["page_num"]), int(args["page_size"])))
        make_log("all_news", all_news)
        for news in all_news:
            news["news_time"] = news["news_time"].strftime("%Y-%m-%d %H:%M:%S")

        response = import_status("SUCCESS_GET_NEWS", "OK")
        response["data"] = all_news
        return response

    def get_abo(self):
        args = request.args.to_dict()
        make_log("args", args)
        true_args = ["id"]
        if judge_keys(true_args, args.keys()) != 200:
            return judge_keys(true_args, args.keys())
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
        args = request.args.to_dict()
        make_log("args", args)
        data = json.loads(request.data)
        make_log("data", data)
        true_data = ["news_title", "news_all", "news_picture", "news_from"]
        if judge_keys(true_data, data.keys()) != 200:
            return judge_keys(true_data, data.keys())
        update_news = self.snews.update_news(args["id"], data)
        make_log("update_news", update_news)
        if not update_news:
            return SYSTEM_ERROR
        return import_status("SUCCESS_UPDATE_NEWS", "OK")

    def upload_files(self):
        formdata = request.form
        make_log("formdata", formdata)
        files = request.files.get("file")

        import platform
        from Fansti.config import Inforcode
        if platform.system() == "Windows":
            rootdir = Inforcode.WindowsRoot
        else:
            rootdir = Inforcode.LinuxRoot + Inforcode.LinuxImgs
        if not os.path.isdir(rootdir):
            os.mkdir(rootdir)
        if "FileType" not in formdata:
            return
        filessuffix = str(files.filename).split(".")[-1]
        index = formdata.get("index", 1)
        filename = formdata.get("FileType") + str(index) + "." + filessuffix
        filepath = os.path.join(rootdir, filename)
        print(filepath)
        files.save(filepath)
        response = import_status("SUCCESS_MESSAGE_SAVE_FILE", "OK")
        url = Inforcode.ip + Inforcode.LinuxImgs + "/" + filename
        print(url)
        response["data"] = url
        return response