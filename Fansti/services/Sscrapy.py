# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Fansti.models.model import AIR_HWYS_JD, AIR_HWYS_LINES
from Fansti.services.SBase import SBase, close_session

class Sscrapy(SBase):

    @close_session
    def get_jd_by_name(self, name):
        return self.session.query(AIR_HWYS_JD.chinesename, AIR_HWYS_JD.englistname, AIR_HWYS_JD.unno,
                                  AIR_HWYS_JD.appearance, AIR_HWYS_JD.appearance2)\
            .filter_by(chinessname=name).first()

    @close_session
    def get_chinessname_by_englishname(self, englishname):
        return self.session.query(AIR_HWYS_JD.chinesename).filter_by(englishname=englishname).first()

    @close_session
    def get_all_by_depa_dest(self, depa=None, dest=None):
        return self.session.query(AIR_HWYS_LINES.depa, AIR_HWYS_LINES.dest, AIR_HWYS_LINES.flight, AIR_HWYS_LINES.date,
                                  AIR_HWYS_LINES.aircraft, AIR_HWYS_LINES.etd, AIR_HWYS_LINES.eta)\
            .filter_by(depa=depa).filter_by(dest=dest).all()

