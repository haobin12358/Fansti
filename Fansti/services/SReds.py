# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Fansti.models.model import WECHAT_RED_COIN, GET_RED_COIN
from Fansti.services.SBase import SBase, close_session

class SReds(SBase):

    @close_session
    def get_my_red_receive(self, login_name):
        return self.session.query(GET_RED_COIN.createtime, GET_RED_COIN.red_id)\
            .filter_by(login_name=login_name).filter_by(status=2).all()

    @close_session
    def get_my_red_rereceive(self, login_name):
        return self.session.query(GET_RED_COIN.createtime, GET_RED_COIN.red_id) \
            .filter_by(login_name=login_name).filter_by(status=1).all()

    @close_session
    def get_my_red_status(self, login_name):
        return self.session.query(GET_RED_COIN.red_id, GET_RED_COIN.status)\
            .filter_by(login_name=login_name).filter(GET_RED_COIN.status >= 0, GET_RED_COIN.status <= 1).all()

    @close_session
    def get_my_red_by_time(self, starttime, endtime):
        return self.session.query(GET_RED_COIN.red_id).filter(GET_RED_COIN.createtime.between(starttime, endtime)).all()

    @close_session
    def get_id_by_red_loginname(self, red, login_name):
        return self.session.query(GET_RED_COIN.id).filter_by(red_id=red).filter_by(login_name=login_name).first()

    @close_session
    def get_red_by_id(self, red_id):
        return self.session.query(WECHAT_RED_COIN.name, WECHAT_RED_COIN.id, WECHAT_RED_COIN.price)\
            .filter_by(id=red_id).first()