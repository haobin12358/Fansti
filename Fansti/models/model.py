# *- coding:utf-8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, Integer, String, Text, Float, DATE, DATETIME
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
    create_time = Column(DATE)                  # 创建时间
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
    __tablename__ = "AIR_HWYS_DCD"
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
    __tablename__ = "AIR_HWYS_FILE"
    id = Column(String(50), primary_key=True)                   # 主键id
    jcno = Column(String(20))                                   # 鉴定单对应id
    content = Column(String(200))                               # 文件备注
    createtime = Column(DATE, default=datetime.datetime.now())  # 创建时间
    filename = Column(String(500))                              # 文件名称

class AIR_HWYS_DCD_JLD(Base):
    __tablename__ = "AIR_HWYS_DCD_JLD"
    id = Column(String(200), primary_key=True)
    jcno = Column(String(50))
    message = Column(String(2000))
    isok = Column(String(100), default='否')
    createtime = Column(DATE, default=datetime.datetime.now())
    dhmes = Column(String(2000))
    mes1 = Column(String(2000))
    mes2 = Column(String(2000))
    mes3 = Column(String(2000))

class AIR_HWYS_PHOTOS(Base):
    __tablename__ = "AIR_HWYS_PHOTOS"
    id = Column(String(200), primary_key=True)          # 主键
    jcno = Column(String(50), nullable=False)           # 进仓单号
    phototype = Column(String(100), nullable=False)     # 照片类型in进仓out出仓weight称重
    photourl = Column(String(200), nullable=False)      # 图片地址
    createtime = Column(DATE, nullable=False)           # 创建时间
    czr = Column(String(100))                           # 处理师傅
    filename = Column(String(100))                      # 文件名称
    filetext = Column(String(100), default="无")        # 文件信息
    photoheadid = Column(String(100))                   # 关联photo_head

class WECHAT_LOGIN(Base):
    __tablename__ = "WECHAT_LOGIN"
    id = Column(String(200), primary_key=True)          # 主键id
    openid = Column(String(200))                        # 微信id
    login_name = Column(String(40))                     # 登录名
    phone = Column(String(32))                          # 手机号
    status = Column(String(10), default="0")            # 绑定状态，1为已绑定
    name = Column(String(200))                          # 微信昵称
    usex = Column(String(200))                          # 微信性别
    city = Column(String(200))                          # 所在城市
    province = Column(String(200))                      # 所在省份
    user_name = Column(String(200))                     # 用户名称
    work_year = Column(String(40))                      # 从业时间
    work_goodat = Column(String(2000))                  # 经验擅长
    user_introduction = Column(String(2000))            # 个人简介
    qq = Column(String(40))                             # 个人QQ
    wechat = Column(String(200))                        # 个人微信
    email = Column(String(200))                         # 个人邮箱

class WECHAT_NEWS(Base):
    __tablename__ = "WECHAT_NEWS"
    id = Column(String(200), primary_key=True)          # 主键id
    news_title = Column(String(200))                    # 新闻标题
    news_all = Column(Text)                             # 新闻详情
    news_picture = Column(String(200))                  # 新闻主图
    news_from = Column(String(200))                     # 新闻来源
    news_time = Column(DATE)                            # 新闻日期
    news_status = Column(String(10))                    # 新闻状态

class AIR_HWYS_JD(Base):
    __tablename__ = "AIR_HWYS_JD"
    id = Column(String(200), primary_key=True)                  # 主键id
    jcno = Column(String(1000))                                 # 进仓编号
    createtime = Column(DATE, default=datetime.datetime.now())  # 创建时间
    endtime = Column(DATE)                                      # 出鉴定日期
    reportno = Column(String(1000))                             # 报告编号
    chinesename = Column(String(2000))                          # 中文品名
    englishname = Column(String(2000))                          # 英文品名
    appearance = Column(String(200))                            # 外观-颜色
    identificationunits = Column(String(200))                   # 鉴定委托单位
    cost = Column(String(200), default="未填写")                # 费用
    remarks = Column(String(2000))                              # 备注
    principal = Column(String(200))                             # 鉴定委托人
    jdtime = Column(DATE)                                       # 做鉴定日期
    singlenode = Column(String(20))                             # 是否结单
    crz = Column(String(200))                                   # 客服人
    unno = Column(String(200))                                  # UN信息
    wphw = Column(String(20))                                   # 危险品/普货
    cz = Column(String(200))                                    # 单据操作者
    flag = Column(String(10))                                   # 是否带入中文品名
    flag2 = Column(String(10))                                  # 是否带入英文品名
    flag3 = Column(String(10))                                  # 是否带入成本费用
    flag4 = Column(String(10), default="0")                     # 展示标识
    flag5 = Column(String(10))                                  # 带入鉴定单
    factory = Column(String(200))                               # 生产厂家
    appearance2 = Column(String(200))                           # 外观-状态
    casno = Column(String(100))                                 # CAS NO号码
    costtype = Column(String(50))                               # 费用种类

class SELECT_INFO(Base):
    __tablename__ = "SELECT_INFO"
    id = Column(String(200), primary_key=True)                  # 主键id
    login_name = Column(String(40))                             # 登录名
    select_name = Column(String(200))                           # 查询名称
    select_value = Column(String(400))                          # 查询内容
    openid = Column(String(200))                                # 微信id

class AIR_HWYS_LINES(Base):
    __tablename__ = "AIR_HWYS_LINES"
    id = Column(String(200), primary_key=True)                  # 主键id
    airline = Column(String(200))                               # 航线编号
    aipcompany = Column(String(200))                            # 航空公司
    airname = Column(String(200))                               # 航空类型
    flight = Column(String(200))                                # 航班编号
    depa = Column(String(50))                                   # 起飞地
    dest = Column(String(50))                                   # 目的地
    mydate = Column(String(50))                                 # 航班日期
    etd = Column(DATE)                                          # 起飞时间
    eta = Column(DATE)                                          # 落地时间
    supporttime = Column(String(100))                           # 交单时间
    aircraft = Column(String(200))                              # 机型
    remark = Column(Text)                                       # 备注

class WECHAT_RED_COIN(Base):
    __tablename__ = "WECHAT_RED_COIN"
    id = Column(String(200), primary_key=True)                  # 主键id
    name = Column(String(1000))                                 # 任务名称
    price = Column(String(10))                                  # 红包金额

class GET_RED_COIN(Base):
    __tablename__ = "GET_RED_COIN"
    id = Column(String(200), primary_key=True)                  # 主键id
    login_name = Column(String(40))                             # 领取人
    createtime = Column(DATE, default=datetime.datetime.now())  # 领取时间
    red_id = Column(String(200))                                # 关联id
    status = Column(String(20))                                 # 红包状态，0为不可领取，1为可领取，2为已领取

class USER_MESSAGE(Base):
    __tablename__ = "USER_MESSAGE"
    id = Column(String(200), primary_key=True)                  # 主键id
    phone = Column(String(40))                                  # 留言人联系方式
    message = Column(Text)                                      # 留言内容

class USER_INVATE(Base):
    __tablename__ = "USER_INVATE"
    id = Column(String(200), primary_key=True)                  # 主键id
    login_name = Column(String(40))                             # 邀请人login_name
    invate_openid = Column(String(200))                         # 被邀请人微信id

class GOODS_RETRUE(Base):
    __tablename__ = "GOODS_RETRUE"
    id = Column(String(200), primary_key=True)                  # 主键id
    login_name = Column(String(40))                             # 登录名
    jcno = Column(String(1000))                                 # 进仓单号
    in_pic = Column(String(10))                                 # 入仓确认状态， 0未确认， 1确认
    out_pic = Column(String(10))                                # 出仓确认状态， 0未确认， 1确认
    weight_pic = Column(String(10))                             # 称重确认状态， 0未确认， 1确认

class USER_DB_USER(Base):
    __tablename__ = "USER_DB_USER"
    user_id = Column(String(40), primary_key=True)
    user_name = Column(String(40), nullable=False)
    login_name = Column(String(40), nullable=False)
    login_password = Column(String(40), nullable=False)
    is_enable = Column(Integer, nullable=False)
    gender_id = Column(String(40))
    birth_date = Column(DATE)
    memo = Column(String(300))
    lock_version = Column(Integer, nullable=False)
    station_id = Column(String(40))
    dept_id = Column(String(40))
    duty_id = Column(String(40))
    work_id = Column(String(40))
    card_id = Column(String(40))
    locale_id = Column(String(40))
    l18n_id = Column(String(100))
    address = Column(String(300))
    postalcode = Column(String(40))
    telephone = Column(String(40))
    handset = Column(String(40))
    email = Column(String(40))
    fax = Column(String(40))
    notify_mode_id = Column(String(40))
    timezone_id = Column(String(40))
    last_login_date = Column(DATE)
    title_id = Column(String(40))
    edu_level_id = Column(String(40))
    skill_level_id = Column(String(40))
    status_id = Column(String(40))
    workgroup_id = Column(String(40))
    work_schedule_id = Column(String(40))
    qq = Column(String(20))
    telephone2 = Column(String(40))
    handset2 = Column(String(40))
    android_id = Column(String(40))

class AIR_HWYS_DGR(Base):
    __tablename__ = "AIR_HWYS_DGR"
    id = Column(String(200), primary_key=True)              # 主键
    unno = Column(String(200))                              # UN号
    unname = Column(String(200))                            # 运输专用名称
    untype = Column(String(40))                             # 类别

class AIR_HWYS_DGR_LEVEL(Base):
    __tablename__ = "AIR_HWYS_DGR_LEVEL"
    id = Column(String(200), primary_key=True)              # 主键
    dgr_id = Column(String(200))                            # 关联外键
    level = Column(String(200))                             # 等级
    airliner_capacity = Column(String(200))                 # 客机容量
    airliner_description_no = Column(String(200))           # 客机说明号
    airliner_is_single = Column(String(200))                # 客机是否可单一
    airfreighter_capacity = Column(String(200))             # 货机容量
    airfreighter_description_no = Column(String(200))       # 货机说明号
    airfreighter_is_single = Column(String(200))            # 货机是否可单一
    message = Column(String(2000))                          # 备注

class AIR_HWYS_DGR_CONTAINER(Base):
    __tablename__ = "AIR_HWYS_DGR_CONTAINER"
    id = Column(String(200), primary_key=True)              # 主键
    dgr_level_id = Column(String(200))                      # 关联外键
    dgr_container = Column(String(200))                     # 容器类型
    dgr_container_capacity = Column(String(200))            # 容量
    dgr_type = Column(String(60))                           # 客机/货机

if __name__ == "__main__":
    Base.metadata.create_all(mysql_engine)