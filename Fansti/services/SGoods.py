# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Fansti.models.model import AIR_HWYS_WTS, AIR_HWYS_DCD, AIR_WAYS_DCD_PHOTOS, AIR_HWYS_FILE, AIR_HWYS_DCD_JLD
from Fansti.services.SBase import SBase, close_session

class SGoods(SBase):

    @close_session
    def get_all_goods_by_user(self, accounts):
        return self.session.query(AIR_HWYS_WTS.ydno, AIR_HWYS_WTS.jcno, AIR_HWYS_WTS.destination, AIR_HWYS_WTS.hxno,
                                  AIR_HWYS_WTS.jsbzcc, AIR_HWYS_WTS.accounts)\
            .filter_by(accounts=accounts).all()

    @close_session
    def get_dctime_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_DCD.dctime).filter_by(jcno=jcno).first()

    @close_session
    def get_in_order_by_jcno(self, jcno):
        return self.session.query(AIR_WAYS_DCD_PHOTOS.photourl, AIR_WAYS_DCD_PHOTOS.czr, AIR_WAYS_DCD_PHOTOS.createtime)\
            .filter_by(jcno=jcno).filter_by(phototype='in').all()

    @close_session
    def get_out_order_by_jcno(self, jcno):
        return self.session.query(AIR_WAYS_DCD_PHOTOS.photourl, AIR_WAYS_DCD_PHOTOS.czr, AIR_WAYS_DCD_PHOTOS.createtime) \
            .filter_by(jcno=jcno).filter_by(phototype='out').all()

    @close_session
    def get_weight_order_by_jcno(self, jcno):
        return self.session.query(AIR_WAYS_DCD_PHOTOS.photourl, AIR_WAYS_DCD_PHOTOS.czr, AIR_WAYS_DCD_PHOTOS.createtime) \
            .filter_by(jcno=jcno).filter_by(phototype='weight').all()

    @close_session
    def get_content_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_FILE.content)\
            .filter(AIR_HWYS_FILE.content.like("报关单"), AIR_HWYS_FILE.jcno == jcno).all()

    @close_session
    def get_awb_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_FILE.content)\
            .filter_by(content='awb').filter_by(jcno=jcno).all()

    @close_session
    def get_jd_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_WTS.jd_date, AIR_HWYS_WTS.jd_time).filter_by(jcno=jcno).first()

    @close_session
    def get_hbdate_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_DCD.hbdate1).filter_by(jcno=jcno).first()

    @close_session
    def get_dhmes_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_DCD_JLD.dhmes).filter_by(jcno=jcno).first()

    @close_session
    def get_goods_abo_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_WTS.ydno, AIR_HWYS_WTS.destination, AIR_HWYS_WTS.jcno, AIR_HWYS_WTS.enhwpm)\
            .filter_by(jcno=jcno).first()

    @close_session
    def get_quantity_weight_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_DCD.quantity, AIR_HWYS_DCD.weight).filter_by(jcno=jcno).first()

    @close_session
    def get_accounts_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_WTS.accounts).filter_by(jcno=jcno).first()