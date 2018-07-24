# *- coding:utf-8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, Integer, String, Text, Float, DATE
from Fansti.config import dbconfig as cfg
import datetime

DB_PARAMS = "{0}://{1}:{2}@{3}:{4}/{5}".format(
    cfg.sqlenginename, cfg.username, cfg.password, cfg.host, cfg.port, cfg.database)
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

class AIR_HWYS_WTS(Base):
    __tablename__ = "AIR_HWYS_WTS"
    id = Column(String(200), primary_key=True)      # 主键id
    ydno = Column(String(20))                       # 运单号125-1423-7580
    jcno = Column(String(20))                       # 进仓编号E1412554QN
    shipper = Column(String(500))                   # 托运人信息
    consignee = Column(String(500))                 # 收件人信息
    notify = Column(String(1500))                   #
    departure = Column(String(50), default='PEK')   # 起运地
    destination = Column(String(50))                # 目的地
    arrivetime = Column(DATE)                       # 到货时间
    transtime = Column(DATE)                        # 起运时间
    company = Column(String(100))                   # 航空公司
    contract = Column(String(50))                   # 合同号
    isbx = Column(String(100))                      # 是否保鲜
    hxno = Column(String(50))                       # 核销单号
    trademode = Column(String(1000))                # 贸易方式
    isbg = Column(String(100))                      # 是否报关
    ists = Column(String(100))                      # 是否退税
    yfdf = Column(String(100))                      # 运费到付
    yfyf = Column(String(100))                      # 运费预付
    isfile = Column(String(100))                    # 是否有随机文件
    tdyj = Column(String(100), default='未填写')    # 提单正本邮寄
    tdcz = Column(String(100))                      # 提单传真
    hycd = Column(String(200))                      # 货源产地
    isphoto = Column(String(50))                    # 是否拍照确认
    jsbzcc = Column(String(2000))                   # 件数包装尺寸
    jzmz = Column(String(1000))                     # 净重毛重
    hwzt = Column(String(500))                      # 货物状态（固态液态）
    wphw = Column(String(10))                       # 危品货物
    pthw = Column(String(10))                       # 普通货物
    hwpm = Column(String(2000))                     # 货物品名（中文）
    instruction = Column(String(500))               # 其他要求
    confirm = Column(String(2000))                  # 空运费杂费确认
    createtime = Column(DATE, default=datetime.datetime.now())# 创建时间
    czr = Column(String(50))                        # 操作人
    xsr = Column(String(50))                        # 销售人
    link_sbd = Column(String(20), default='申报单') # 申报单链接
    link_dcd = Column(String(20), default='订舱单') # 订舱单链接
    link_tys = Column(String(20), default='地面托运书')# 托运书链接
    link_yd = Column(String(20), default='运单')      # 运单链接
    link_qrd = Column(String(20), default='账单')     # 费用单链接
    link_file = Column(String(20), default='废单')    # 废单链接
    link_bq = Column(String(20), default='标签')      # 标签链接
    status = Column(String(10), default='0')          # 货单状态（911代表废单） TODO
    accounts = Column(String(100))                    #
    link_hkqr = Column(String(20), default='成本')     # 成本链接
    link_ajd = Column(String(20), default='安检单')    # 安检单链接
    jd_date = Column(DATE)                            # 交单日期
    flag_date = Column(DATE)                            # 安卓端上传图片标识日期
    enhwpm = Column(String(4000))                       # 货物品名（英文）
    wpzd = Column(String(200))                          # 根据危险品普品带入账单信息
    jd_time = Column(DATE)                              # 交单时间精确
    consignore = Column(String(100))                    # 委托人
    message_flag = Column(String(30), default='1')      # 短信发送标识 TODO
    wh_require = Column(String(1000))                   # 仓库要求
    star = Column(String(10))                           # star
    photo_require_source = Column(String(10))           # 照片确认来源，手机端确认照片后，该字段为1
    con_flag = Column(String(10))                       # 填报信息为托书添加的，本字段置为1
    msg_flag = Column(String(10))                       # 是否已经发送微信模块消息标识，已发送后该字段置为1
    dmczlx = Column(String(40))                         # 地面操作类型
    czlx_type = Column(String(40))                      # 地面操作分类
    proportion = Column(String(60))                     # 货物比重
    declare = Column(String(500))                       # 申报单位
    to_pay = Column(String(10))                         # 是否买单
    is_urgent = Column(String(10))                      # 是否紧急
    act_flag = Column(String(10))                       # 打代理标识
    handinfo = Column(String(500))                      #
    link_sbd_file = Column(String(20), default='申报文件')# 申报文件
    usic = Column(String(100))
    hcsb = Column(String(100))

class AIR_HWYS_DCD(Base):
    __tablename__ = 'AIR_HWYS_DCD'
    id = Column(String(200), primary_key=True)          # 主键id
    tname = Column(String(100))                         # 收件人姓名
    ttel = Column(String(50))                           # 收件人电话
    tfax = Column(String(50))                           # 收件人传真
    fname = Column(String(100))                         # 寄件人姓名
    ftel = Column(String(50))                           # 寄件人电话
    ffax = Column(String(50))                           # 寄件人传真
    ydno = Column(String(20))                           # 运单号
    destination = Column(String(50))                    # 目的港
    quantity = Column(String(100))                      # 件数
    weight = Column(String(100))                        # 重量
    volume = Column(String(100))                        # 体积
    hwsixe = Column(String(200))                        # 尺寸
    hwpm = Column(String(2000))                         # 货物品名
    flight = Column(String(200))                        # 航班
    charge = Column(String(500))                        # 运价
    dctime = Column(DATE)                               # 订舱日期
    createtime = Column(DATE, default=datetime.datetime.now())  # 创建时间
    jcno = Column(String(20))                           # 进仓编号
    crz = Column(String(50))                            # 操作人
    flightdate = Column(DATE)                           #
    bz1 = Column(String(200))                           #
    bz2 = Column(String(500))                           #
    service = Column(String(100))                       #
    cbd_no = Column(String(50))                         #
    select1 = Column(String(500))                       #
    iskh = Column(String(100))                          #
    iszf = Column(String(100))                          #
    hbpf1 = Column(String(1000))                        #
    hbdate1 = Column(DATE)                              #
    hbpf2 = Column(String(1000))                        #
    hbdate2 = Column(DATE)                              #
    hbpf3 = Column(String(1000))                        #
    hbdate3 = Column(DATE)                              #
    hbbz1 = Column(String(500))                         #
    hbbz2 = Column(String(500))                         #
    hbbz3 = Column(String(500))                         #
    unno = Column(String(500))                          #
    risk = Column(String(500))                          #
    pack = Column(String(500))                          #
    packno = Column(String(500))                        #
    flag = Column(String(200))                          #
    dxflag = Column(String(10), default='0')            # 短信发送识别标识1为发送成功
    dh_dx_flag = Column(String(10), default='0')        # 到货信息发送标识2为发送成功
    tnameid = Column(String(200))                       #
    type = Column(String(50))                           # 订舱单货物重量分类
    type2 = Column(String(50))                          # 订舱单货物重量分类
    charge2 = Column(String(500))                       # 运价2
    fname2 = Column(String(100))                        # 主订舱员
    hbdate11 = Column(String(100))                      # 交单截止时刻（针对一程信息）

class AIR_HWYS_FILE(Base):
    __tablename__ = 'AIR_HWYS_FILE'
    id = Column(String(50), primary_key=True)                   # 主键id
    jcno = Column(String(20))                                   # 鉴定单对应id
    content = Column(String(200))                               # 文件备注
    createtime = Column(DATE, default=datetime.datetime.now())  # 创建时间
    filename = Column(String(500))                              # 文件名称

class AIR_HWYS_DCD_JLD(Base):
    __tablename__ = 'AIE_HWYS_DCD_JLD'
    id = Column(String(200), primary_key=True)
    jcno = Column(String(50))
    message = Column(String(2000))
    isok = Column(String(100), default='否')
    createtime = Column(DATE, default=datetime.datetime.now())
    dhmes = Column(String(2000))
    mes1 = Column(String(2000))
    mes2 = Column(String(2000))
    mes3 = Column(String(2000))