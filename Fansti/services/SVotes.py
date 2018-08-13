# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy import func
from Fansti.models.model import Votes as VS, Vote as VO, Votenotes as VN, VoteChoice as VC
from Fansti.services.SBase import SBase, close_session


class SVotes(SBase):
    def __init__(self):
        super(SVotes, self).__init__()

    @close_session
    def get_votes(self, vsid):
        return self.session.query(
            VS.vsid, VS.vscontent, VS.vsname, VS.vsstarttime, VS.vsendtime, VS.vsurl).filter(
            VS.vsid == vsid).first()

    @close_session
    def get_vote(self, vsid, vono=1):
        return self.session.query(
            VO.void, VO.votext, VO.votype, VO.vono, VO.voisnull, VO.vsid, VO.vounit, VO.vobackground).filter(
            VO.vsid == vsid, VO.vono == vono).first()

    @close_session
    def get_all_votes(self):
        return self.session.query(
            VS.VSid, VS.VScontent, VS.VSname, VS.VSstartTime, VS.VSendTime, VS.VSurl, VS.VShead, VS.VSbannel).all()

    @close_session
    def get_votechoisce(self, void):
        return self.session.query(VC.vcid, VC.vcno, VC.vctext, VC.vcnext, VC.vctype).filter(VC.void == void).all()

    @close_session
    def get_count(self, vsid):
        return self.session.query(func.count(VO.void)).filter(VO.vsid == vsid).scalar()

    @close_session
    def get_Votenotes(self, vsid, usid):
        return self.session.query(
            VN.VNid, VN.VSid, VN.USid, VN.VNtime
        ).filter(VN.USid == usid, VN.VSid == vsid).scalar()