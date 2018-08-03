# *- coding:utf8 *-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, String, DATE
from sqlalchemy.orm import sessionmaker
database = "ORCL"
host = "122.233.181.49"
port = "1521"
username = "C##M"
password = "root"
charset = "utf8"
sqlenginename = 'oracle'

DB_PARAMS = "{0}://{1}:{2}@{3}:{4}/{5}".format(
    sqlenginename, username, password, host, port, database)
mysql_engine = create_engine(DB_PARAMS, echo=False)
Base = declarative_base()

class D_MESSAGE_USER(Base):
    __tablename__ = 'D_MESSAGE_USER'
    id = Column(String(32), primary_key=True)   # ID主键
    compnay = Column(String(200))               # 客户所在公司
    username = Column(String(100))              # 客户名称
    czr = Column(String(100))                   # 负责客服
    phone = Column(String(32))                  # 客户电话
    pet_name = Column(String(40))               # 客户昵称
    user_wx = Column(String(40))                # 客户微信号
    xsr = Column(String(100))                   # 负责销售
    login_name = Column(String(40))             # 登录名
    login_password = Column(String(60))         # 登录密码
    account_id = Column(String(40))             #
    user_type = Column(String(2))               # 用户类型
    account_type = Column(String(2))            #
    wx_post = Column(String(40))                # 微信推送
    login_url = Column(String(200))             # 免登陆URL
    create_time = Column(String(DATE))          # 创建时间
    create_user = Column(String(40))            # 创建人

db_session = sessionmaker(bind=mysql_engine)


class SUsers():
    def __init__(self):
        self.session = db_session()

    def get_name_password_phone(self):
        return self.session.query(D_MESSAGE_USER.login_name, D_MESSAGE_USER.login_password, D_MESSAGE_USER.phone).first()

if __name__ == "__main__":
    suser = SUsers()
    print suser.get_name_password_phone()