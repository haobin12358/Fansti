# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
from Fansti.models.model import D_MESSAGE_USER
from Fansti.common.TransformToList import trans_params
from Fansti.services.SBase import SBase, close_session

class SUsers(SBase):

    @close_session
    def get_all(self):
        return self.session.query(D_MESSAGE_USER.login_name).all()

    def get(self):
        try:
            import cx_Oracle  # 导入模块
            db = cx_Oracle.connect('C##M/root@localhost:1521/C##M')
            cursor = db.cursor()
            cursor.excute("select user_type from d_message_user")
            row = cursor.fetchall()
            for key in row:
                for v in key:
                    print v
        except Exception as e:
            print(1)
            print(e.message)


if __name__ == '__main__':
    suser = SUsers()
    print(suser.get_all())