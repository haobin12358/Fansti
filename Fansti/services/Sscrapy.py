# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Fansti.models.model import AIR_HWYS_JD, AIR_HWYS_LINES, SELECT_INFO, AIR_HWYS_DGR, AIR_HWYS_DGR_LEVEL, \
    AIR_HWYS_DGR_CONTAINER, AIR_HWYS_TACT
from Fansti.services.SBase import SBase, close_session

class Sscrapy(SBase):

    @close_session
    def get_jd_by_name(self, name):
        return self.session.query(AIR_HWYS_JD.chinesename, AIR_HWYS_JD.englishname, AIR_HWYS_JD.unno,
                                  AIR_HWYS_JD.appearance, AIR_HWYS_JD.appearance2)\
            .filter_by(chinesename=name).first()

    @close_session
    def get_chinessname_by_englishname(self, englishname):
        return self.session.query(AIR_HWYS_JD.chinesename).filter_by(englishname=englishname).first()

    @close_session
    def get_all_by_depa_dest(self, depa=None, dest=None):
        return self.session.query(AIR_HWYS_LINES.depa, AIR_HWYS_LINES.dest, AIR_HWYS_LINES.flight, AIR_HWYS_LINES.mydate,
                                  AIR_HWYS_LINES.aircraft, AIR_HWYS_LINES.etd, AIR_HWYS_LINES.eta)\
            .filter_by(depa=depa).filter_by(dest=dest).all()

    @close_session
    def get_all_select(self, page_num, page_size, select_name):
        return self.session.query(SELECT_INFO.login_name, SELECT_INFO.openid, SELECT_INFO.select_name)\
            .filter_by(select_name=select_name).offset(page_size * (page_num - 1)).limit(page_size).all()

    @close_session
    def get_dgr_by_unno(self, unno):
        return self.session.query(AIR_HWYS_DGR.id, AIR_HWYS_DGR.unno, AIR_HWYS_DGR.unname, AIR_HWYS_DGR.untype)\
            .filter_by(unno=unno).first()

    @close_session
    def get_dgr_level_by_dgrid(self, dgr_id):
        return self.session.query(AIR_HWYS_DGR_LEVEL.id, AIR_HWYS_DGR_LEVEL.airfreighter_capacity,
                                  AIR_HWYS_DGR_LEVEL.airfreighter_description_no,
                                  AIR_HWYS_DGR_LEVEL.airfreighter_is_single, AIR_HWYS_DGR_LEVEL.airliner_capacity,
                                  AIR_HWYS_DGR_LEVEL.airliner_description_no, AIR_HWYS_DGR_LEVEL.airliner_is_single,
                                  AIR_HWYS_DGR_LEVEL.message, AIR_HWYS_DGR_LEVEL.dgr_level)\
            .filter_by(dgr_id=dgr_id).all()

    @close_session
    def get_dgr_container_by_levelid(self, dgr_level_id):
        return self.session.query(AIR_HWYS_DGR_CONTAINER.dgr_container, AIR_HWYS_DGR_CONTAINER.dgr_container_capacity,
                                  AIR_HWYS_DGR_CONTAINER.dgr_type)\
            .filter_by(dgr_level_id=dgr_level_id).all()

    @close_session
    def get_airline_by_flight(self, airflight):
        return self.session.query(
            AIR_HWYS_LINES.id, AIR_HWYS_LINES.airline, AIR_HWYS_LINES.aircompany, AIR_HWYS_LINES.airname,
            AIR_HWYS_LINES.flight, AIR_HWYS_LINES.depa, AIR_HWYS_LINES.dest, AIR_HWYS_LINES.mydate, AIR_HWYS_LINES.etd,
            AIR_HWYS_LINES.eta, AIR_HWYS_LINES.supporttime, AIR_HWYS_LINES.aircraft, AIR_HWYS_LINES.remark
        ).filter(AIR_HWYS_LINES.flight == airflight).first()

    @close_session
    def update_airline(self, airflight, airlines):
        return self.session.query(AIR_HWYS_LINES).filter(AIR_HWYS_LINES.flight == airflight).update(airlines)

    @close_session
    def get_tact_by_three_code(self, three_code):
        return self.session.query(AIR_HWYS_TACT.three_code, AIR_HWYS_TACT.city, AIR_HWYS_TACT.state,
                                  AIR_HWYS_TACT.country, AIR_HWYS_TACT.freight, AIR_HWYS_TACT.chinese_position)\
            .filter_by(three_code=three_code).first()
