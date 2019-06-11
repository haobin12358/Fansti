# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Fansti.models.model import D_MESSAGE_USER, WECHAT_LOGIN, USER_MESSAGE, USER_INVATE, USER_DB_USER
from Fansti.services.SBase import SBase, close_session
from sqlalchemy import or_

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
    def get_compnay_by_loginname_super(self, login_name):
        return self.session.query(D_MESSAGE_USER.compnay).filter_by(login_name=login_name).first()

    @close_session
    def get_wechat_login_by_phone(self, phone):
        return self.session.query(WECHAT_LOGIN.id, WECHAT_LOGIN.login_name).filter_by(phone=phone).first()

    @close_session
    def get_user_message(self, page_size, page_num, time_start=None, time_end=None):
        return self.session.query(USER_MESSAGE.phone, USER_MESSAGE.message)\
            .offset((page_num - 1) * page_size).limit(page_size).all()

    @close_session
    def get_all_user_message(self):
        return self.session.query(USER_MESSAGE.phone).all()

    @close_session
    def get_invate_by_login_name(self, openid, page_size, page_num):
        return self.session.query(USER_INVATE.invate_openid).filter_by(args_openid=openid)\
            .offset(page_size * (page_num - 1)).limit(page_size)\
            .all()

    @close_session
    def get_invate_abo_by_openid(self, openid):
        return self.session.query(WECHAT_LOGIN.phone, WECHAT_LOGIN.name).filter_by(openid=openid).first()

    @close_session
    def get_custom_by_xsr(self, xsr):
        return self.session.query(USER_DB_USER.user_name, USER_DB_USER.telephone, USER_DB_USER.qq, USER_DB_USER.email)\
            .filter_by(user_name=xsr).first()

    @close_session
    def get_personal_by_openid(self, openid):
        return self.session.query(WECHAT_LOGIN.user_name, WECHAT_LOGIN.work_year, WECHAT_LOGIN.work_goodat,
                                  WECHAT_LOGIN.user_introduction, WECHAT_LOGIN.phone, WECHAT_LOGIN.qq,
                                  WECHAT_LOGIN.wechat, WECHAT_LOGIN.email)\
            .filter_by(openid=openid).first()

    @close_session
    def get_id_by_openid(self, invate_openid):
        return self.session.query(USER_INVATE.id).filter_by(invate_openid=invate_openid).first()

    @close_session
    def update_wechat_login_by_phone(self, phone, wl):
        return self.session.query(WECHAT_LOGIN).filter(WECHAT_LOGIN.phone == phone).update(wl)

    @close_session
    def get_user_type(self, login_name):
        return self.session.query(D_MESSAGE_USER.user_type, D_MESSAGE_USER.location)\
            .filter(D_MESSAGE_USER.login_name == login_name).first()

    @close_session
    def get_user_by_openid(self, openid):
        """open获取用户"""
        user = self.session.query(WECHAT_LOGIN).filter(WECHAT_LOGIN.openid == openid).first()
        self.session.expunge_all()
        return user

    @close_session
    def get_user_name(self, login_name):
        return self.session.query(D_MESSAGE_USER.username).filter_by(login_name=login_name).first()

    @close_session
    def get_packer_by_select(self, select_name, location):
        packer = self.session.query(D_MESSAGE_USER.id, D_MESSAGE_USER.username)\
            .filter(or_(D_MESSAGE_USER.user_type == "5", D_MESSAGE_USER.user_type == "4"))\
            .filter(D_MESSAGE_USER.location == location)
        if select_name:
            packer = packer.filter(D_MESSAGE_USER.username.like("%{0}%".format(select_name))).all()
        return packer

    @close_session
    def get_user_openid(self, login_name):
        return self.session.query(D_MESSAGE_USER.open_id).filter_by(login_name=login_name).first()

    @close_session
    def update_d_message_user(self, id, user):
        self.session.query(D_MESSAGE_USER).filter_by(id=id).update(user)
        self.session.commit()
        return True

    @close_session
    def get_id_by_name(self, login_name):
        return self.session.query(D_MESSAGE_USER.id).filter_by(login_name=login_name).first()