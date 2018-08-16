# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from Fansti.config.response import SYSTEM_ERROR, PARAMS_MISS
from Fansti.common.import_status import import_status
from Fansti.common.timeformate import get_db_time_str
from Fansti.common.get_model_return_list import get_model_return_dict as todict, get_model_return_list as tolist


class CVotes():
    conversion_VOunit = {1300: "站"}
    conversion_VOtype = {1001: "单选题", 1002: '多选题', 1003: '填空题'}
    conversion_VOunit_reverse = {k: v for v, k in conversion_VOunit.items()}
    conversion_VOtype_reverse = {k: v for v, k in conversion_VOtype.items()}

    def __init__(self):
        from Fansti.services.SVotes import SVotes
        self.svotes = SVotes()
        from Fansti.services.SUsers import SUsers
        self.susers = SUsers()
        self.title = '============{0}============'

    def get_vote(self):
        args = request.args.to_dict()
        print(self.title.format('args'))
        print(args)
        print(self.title.format('args'))

        if "VSid" not in args:
            return PARAMS_MISS

        vono = args.get("VOno") if args.get("VOno") else 1
        vsid = args.get("VSid")
        try:
            votes = self.svotes.get_votes(vsid)
            print(self.title.format('votes'))
            print(votes)
            print(self.title.format('votes'))
            count = self.svotes.get_count(vsid)
            print(self.title.format('count'))
            print(count)
            print(self.title.format('count'))
            vote = todict(self.svotes.get_vote(vsid, vono))
            # vote["votext"] = vote["votext"].decode("gbk").encode("utf8")
            print(self.title.format("vote"))
            print(vote)
            print(self.title.format("vote"))
            # 获取下一题no
            if int(vote.get("vono")) <= count:
                if vote.get("votype") < 1003:
                    votechoice_list = tolist(self.svotes.get_votechoisce(vote.get("void")))
                    if vote.get("votype") < 1002:
                        for votechoice in votechoice_list:
                            # votechoice["vctext"] = votechoice["vctext"].decode("gbk").encode("utf8")
                            if not votechoice.get("vcnext"):
                                votechoice["vcnext"] = int(vote.get("vono")) + 1
                    else:
                        vote["vcnext"] = int(vote.get("vono")) + 1
                    vote["votechoice"] = votechoice_list
                else:
                    vote["vcnext"] = int(vote.get("vono")) + 1
            else:
                vote["vcnext"] = ""
            vote["vounit"] = self.conversion_VOunit.get(vote.get("vounit"))
            vote["votype"] = self.conversion_VOtype.get(vote.get('votype', 1001))
            response = import_status("SUCCESS_MESSAGE_GET_VOTE", "OK")

            vote["progress"] = int(float(vote.get("vono")) / float(count) * 100)
            response["data"] = vote
            return response
        except Exception as e:
            print(self.title.format("get vote"))
            print(e)
            print(self.title.format("get vote"))
            return SYSTEM_ERROR

    def make_random_code(self, m, n):
        import random
        random_code = ""
        while len(random_code) < m:
            a = random.randint(97, 122)
            a = chr(a)
            random_code = random_code + a
        while len(random_code) < n:
            a = random.randint(0, 9)
            random_code = random_code + str(a)
        return random_code

    def make_vote(self):
        data = json.loads(request.data)
        print(self.title.format('data'))
        print(data)
        print(self.title.format('data'))
        openid = data.get("openid")

        vntime = get_db_time_str()
        vnid = str(uuid.uuid4())
        self.svotes.add_model("Votenotes", **{
            "vnid": vnid,
            "vsid": data.get("VSid"),
            "openid": openid,
            "vntime": vntime
        })
        VoteResult = data.get("USchoose")
        for vr in VoteResult:

            self.svotes.add_model("VoteResult", **{
                "vrid": str(uuid.uuid1()),
                "vnid": vnid,
                "void": vr.get("VOid"),
                "vrchoice": vr.get("VRchoice"),
                "vrabo": vr.get("VRabo")
            })

        # TODO 更新红包状态
        response = import_status("SUCCESS_MESSAGE_NEW_VOTE", "OK")
        return response
