# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Fansti.models.model import WECHAT_RED_COIN, GET_RED_COIN
from Fansti.services.SBase import SBase, close_session

class SReds(SBase):

    @close_session
    def get_my_red_receive(self, login_name):
        return self.session.query(GET_RED_COIN.createtime, GET_RED_COIN.red_id, GET_RED_COIN.id)\
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
        return self.session.query(GET_RED_COIN.red_id)\
            .filter(GET_RED_COIN.createtime.between(starttime, endtime), GET_RED_COIN.status == 2).all()

    @close_session
    def get_id_by_red_loginname(self, red, login_name):
        return self.session.query(GET_RED_COIN.id).filter_by(red_id=red).filter_by(login_name=login_name).first()

    @close_session
    def get_red_by_id(self, red_id):
        return self.session.query(WECHAT_RED_COIN.name, WECHAT_RED_COIN.id, WECHAT_RED_COIN.price)\
            .filter_by(id=red_id).first()

    @close_session
    def get_id_by_redname(self, red_name):
        return self.session.query(WECHAT_RED_COIN.id).filter_by(name=red_name).first()

    @close_session
    def get_myred_by_redid(self, red_id):
        return self.session.query(GET_RED_COIN.id, GET_RED_COIN.status, GET_RED_COIN.login_name, GET_RED_COIN.createtime)\
            .filter_by(red_id=red_id).first()

    @close_session
    def update_myred(self, red_id, myred):
        self.session.query(GET_RED_COIN).filter_by(red_id=red_id).update(myred)
        return True

    @close_session
    def get_red_all(self):
        return self.session.query(WECHAT_RED_COIN.id, WECHAT_RED_COIN.name, WECHAT_RED_COIN.price).all()

    @close_session
    def get_userred_by_loginname_redid(self, loginname, redid, status=1):
        """根据用户名, 红包id, 获取用户红包"""
        user_red = self.session.query(GET_RED_COIN).filter(
            GET_RED_COIN.login_name == loginname,
            GET_RED_COIN.red_id == redid,
            GET_RED_COIN.status == status
        ).first()
        self.session.expunge_all()
        return user_red

    @close_session
    def get_userred_by_id(self, id):
        user_red = self.session.query(GET_RED_COIN).filter(
            GET_RED_COIN.id == id
        ).first()
        self.session.expunge_all()
        return user_red

    @close_session
    def get_red_new_by_id(self, id):
        """根据红包id获取红包, 新方法"""
        red = self.session.query(WECHAT_RED_COIN).filter(WECHAT_RED_COIN.id == id).first()
        self.session.expunge_all()
        return red

    @close_session
    def update_user_red_by_id(self, id, data):
        """根据用户名, 红包id, 获取用户红包"""
        return self.session.query(GET_RED_COIN).filter(
            GET_RED_COIN.id == id
        ).update(data)


