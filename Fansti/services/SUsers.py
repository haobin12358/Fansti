# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Fansti.models.model import D_MESSAGE_USER, WECHAT_LOGIN, USER_MESSAGE, USER_INVATE
from Fansti.services.SBase import SBase, close_session

class SUsers(SBase):
    @close_session
    def get_name_password_phone(self, login_name):
        return self.session.query(D_MESSAGE_USER.login_name, D_MESSAGE_USER.login_password, D_MESSAGE_USER.phone)\
            .filter_by(login_name=login_name).first()

    @close_session
    def update_phone_by_name(self, login_name, phone_args):
        self.session.query(D_MESSAGE_USER).filter_by(login_name=login_name).update(phone_args)
        return True

    @close_session
    def get_wechat_login(self, openid):
        return self.session.query(WECHAT_LOGIN.login_name, WECHAT_LOGIN.status, WECHAT_LOGIN.phone)\
            .filter_by(openid=openid).first()

    @close_session
    def update_wechat_login(self, openid, wechat_args):
        self.session.query(WECHAT_LOGIN).filter_by(openid=openid).update(wechat_args)
        return True

    @close_session
    def get_wechat_login_by_openid(self, openid):
        return self.session.query(WECHAT_LOGIN.login_name, WECHAT_LOGIN.openid, WECHAT_LOGIN.status)\
            .filter_by(openid=openid).first()

    @close_session
    def get_compnay_by_loginname(self, login_name):
        return self.session.query(D_MESSAGE_USER.compnay).filter_by(login_name=login_name).first()

    @close_session
    def get_wechat_login_by_phone(self, phone):
        return self.session.query(WECHAT_LOGIN.id).filter_by(phone=phone).first()

    @close_session
    def get_user_message(self, page_size, page_num, time_start=None, time_end=None):
        return self.session.query(USER_MESSAGE.phone, USER_MESSAGE.message)\
            .offset((page_num - 1) * page_size).limit(page_size).all()

    @close_session
    def get_all_user_message(self):
        return self.session.query(USER_MESSAGE.phone).all()

    @close_session
    def get_invate_by_login_name(self, login_name):
        return self.session.query(USER_INVATE.login_name).filter_by(login_name=login_name).all()

    @close_session
    def get_invate_abo_by_openid(self, openid):
        return self.session.query(WECHAT_LOGIN.phone, WECHAT_LOGIN.name).filter_by(openid=openid).first()