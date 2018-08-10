# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from Fansti.config.response import SYSTEM_ERROR, PARAMS_MISS
from Fansti.common.import_status import import_status
# from LoveBreakfast.common.TransformToList import add_model
from Fansti.common.timeformate import get_db_time_str, get_web_time_str, format_forweb_no_HMS
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
            time_now = get_db_time_str()
            # 答题时间判断
            if votes.VSstartTime and votes.VSstartTime > time_now:
                return import_status("error_vote_time", "LOVEBREAKFAST_ERROR", "error_vote_time_start")
            if votes.VSendTime and votes.VSendTime < time_now:
                return import_status("error_vote_time", "LOVEBREAKFAST_ERROR", "error_vote_time_end")

            vote = todict(self.svotes.get_vote(vsid, vono))
            print(self.title.format("vote"))
            print(vote)
            print(self.title.format("vote"))
            # 获取下一题no
            if int(vote.get("VOno")) < count:
                if vote.get("VOtype") < 1003:
                    votechoice_list = tolist(self.svotes.get_votechoisce(vote.get("VOid")))
                    if vote.get("VOtype") < 1002:
                        for votechoice in votechoice_list:
                            if not votechoice.get("VCnext"):
                                votechoice["VCnext"] = int(vote.get("VOno")) + 1
                    else:
                        vote["VCnext"] = int(vote.get("VOno")) + 1
                    vote["votechoice"] = votechoice_list
                else:
                    vote["VCnext"] = int(vote.get("VOno")) + 1
            else:
                vote["VCnext"] = ""
            vote["VOunit"] = self.conversion_VOunit.get(vote.get("VOunit"))
            vote["VOtype"] = self.conversion_VOtype.get(vote.get('VOtype', 1001))
            response = import_status("SUCCESS_MESSAGE_GET_VOTE", "OK")

            vote["progress"] = int(float(vote.get("VOno")) / float(count) * 100)
            response["data"] = vote
            return response
        except Exception as e:
            print(self.title.format("get vote"))
            print(e.message)
            print(self.title.format("get vote"))
            return SYSTEM_ERROR

    def get_host(self):
        args = request.args.to_dict()
        print(self.title.format('args'))
        print(args)
        print(self.title.format('args'))

        if "VSid" not in args:
            return PARAMS_MISS
        vsid = args.get("VSid")
        votes = todict(self.svotes.get_votes(vsid))
        print(self.title.format('votes'))
        print(votes)
        print(self.title.format('votes'))

        # votes.pop("VSstartTime")
        # votes.pop("VSendTime")
        time_now = get_db_time_str()
        time_status = "时间没问题"
        time_status_code = 200
        if votes.get("VSstartTime") and time_now < votes.get("VSstartTime"):
            time_status_code = 405601
            time_status = "答题时间未到"
        if votes.get("VSendTime") and time_now > votes.get("VSendTime"):
            time_status_code = 405602
            time_status = "答题时间已超"

        votes["VSstartTime"] = get_web_time_str(votes.get("VSstartTime"), format_forweb_no_HMS)

        votes["VSendTime"] = get_web_time_str(votes.get("VSendTime"), format_forweb_no_HMS)
        votes["VStime"] = "2018-08-10"
        votes["TimeStatus"] = time_status
        votes["TimeStatusCode"] = time_status_code
        response = import_status("SUCCESS_MESSAGE_GET_VOTE", "OK")
        response["data"] = votes
        return response

    def make_password(self):
        return self.make_random_code(3, 8)

    def make_invate_code(self):
        USinvate = self.susers.get_all_invate_code()
        while True:
            invate_code = self.make_random_code(3, 7)
            if invate_code not in USinvate:
                break
        return invate_code

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
        usertel = data.get("UStelphone")
        username = data.get("USname")

        user = self.susers.get_uid_by_utel(usertel)

        print(self.title.format('data'))
        print(data)
        print(self.title.format('data'))

        if not user:
            # 注册+免单优惠券
            USinvate = self.make_invate_code()
            print(self.title.format('USinvate'))
            print(USinvate)
            print(self.title.format('USinvate'))

            USpassword = self.make_password()

            print(self.title.format('USpassword'))
            print(USpassword)
            print(self.title.format('USpassword'))

            user = str(uuid.uuid1())
            self.susers.add_model("Users", **{
                "USid": user,
                "UStelphone": usertel,
                "USpassword": USpassword,
                "USname": username,
                "UScoin": 999.99,
                "USinvatecode": USinvate
            })
        vn = self.svotes.get_Votenotes(data.get("VSid"), user)
        if vn:
            return import_status("ERROR_MESSAGE_REPEAT_VOTE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_REPEAT_VOTE")
        vntime = get_db_time_str()
        vnid = str(uuid.uuid1())
        self.svotes.add_model("Votenotes", **{
            "VNid": vnid,
            "VSid": data.get("VSid"),
            "USid": user,
            "VNtime": vntime
        })
        VoteResult = data.get("USchoose")
        for vr in VoteResult:
            if not isinstance(vr.get("VRchoice"), basestring):
                vr["VRchoice"] = json.dumps(vr.get("VRchoice"))

            self.svotes.add_model("VoteResult", **{
                "VRid": str(uuid.uuid1()),
                "VNid": vnid,
                "VOid": vr.get("VOid"),
                "VRchoice": vr.get("VRchoice"),
                "VRabo": vr.get("VRabo")
            })

        self.susers.add_model("Cardpackage", **{
            "CAid": str(uuid.uuid1()),
            "USid": user,
            "CAstatus": 2,
            "CAstart": get_db_time_str(),
            "CAend": "20181231235959",
            "COid": "123",
        })
        response = import_status("SUCCESS_MESSAGE_NEW_VOTE", "OK")
        response["data"] = {
            "UStelphone": usertel,
            "USpassword": self.susers.get_upwd_by_utel(usertel),
        }
        return response
