# *- coding:utf-8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, Integer, String, Text, Float, DATE, DATETIME
from sqlalchemy.dialects.oracle import NUMBER
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
    location = Column(String(40))               # 区域标识
    open_id = Column(String(40))                # 微信授权

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
    accounts = Column(String(100))                    # 客户名
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
    is_delay = Column(String(10))

class AIR_HWYS_PHOTOS(Base):
    __tablename__ = "AIR_HWYS_PHOTOS"
    id = Column(String(200), primary_key=True)          # 主键
    jcno = Column(String(50), nullable=False)           # 进仓单号
    phototype = Column(String(100), nullable=False)     # 照片类型in进仓out出仓weight称重
    photourl = Column(String(200), nullable=False)      # 图片地址
    createtime = Column(DATETIME, nullable=False)           # 创建时间
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
    news_time = Column(DATETIME)                        # 新闻日期
    news_status = Column(String(10))                    # 新闻状态{0不可用1可用}

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
    create_time = Column(String(100))                           # 创建日期

class AIR_HWYS_LINES(Base):
    __tablename__ = "AIR_HWYS_LINES"
    id = Column(String(200), primary_key=True)                  # 主键id
    airline = Column(String(200))                               # 航线编号
    aircompany = Column(String(200))                            # 航空公司
    airname = Column(String(200))                               # 航空类型
    flight = Column(String(200))                                # 航班编号
    depa = Column(String(50))                                   # 起飞地
    dest = Column(String(50))                                   # 目的地
    mydate = Column(String(50))                                 # 航班日期
    etd = Column(String(50))                                    # 起飞时间
    eta = Column(String(50))                                    # 落地时间
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
    args_openid = Column(String(200))                            # 邀请人微信id
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
    dgr_level = Column(String(200))                         # 等级
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
    dgr_container_message = Column(String(2000))            #

class AIR_HWYS_TACT(Base):
    __tablename__ = "AIR_HWYS_TACT"
    id = Column(String(200), primary_key=True)
    three_code = Column(String(200))                        # 三字码
    city = Column(String(200))                              # 城市名
    state = Column(String(200))                             # 州名
    country = Column(String(200))                           # 国家名
    freight = Column(String(2000))                          # 运费
    chinese_position = Column(String(2000))                 # 中文名称及地理位置

class Votes(Base):
    __tablename__ = "Votes"
    vsid = Column(String(64), primary_key=True)
    vsname = Column(Text, nullable=False)  # 问卷名称
    vscontent = Column(Text)               # 问卷描述
    vsstarttime = Column(String(14))       # 起始时间
    vsendtime = Column(String(14))         # 结束时间
    vsurl = Column(Text)                   # 前端路由
    vshead = Column(Text)                  # 问卷icon
    vsbannel = Column(Text)                # 问卷宣传banner


class Vote(Base):
    __tablename__ = "Vote"
    void = Column(String(64), primary_key=True)
    votext = Column(Text, nullable=False)
    votype = Column(Integer, nullable=False)    # 问题类型 {1001：单选题，1002： 多选题， 1003： 填空题}
    vono = Column(String(2), nullable=False)    # 问题编号
    voisnull = Column(Integer, nullable=False)  # 是否可空 {1100： 不可空， 1101：可空}
    vounit = Column(Integer)                    # 填空题后可能涉及的单位 {1300: 站}
    voappend = Column(Text)                     # 如果是填空题，后面的补充内容
    vsid = Column(String(64), nullable=False)   # 问卷id
    vobackground = Column(Text)                  # 背景图


class VoteChoice(Base):
    __tablename__ = "VoteChoice"
    vcid = Column(String(64), primary_key=True)
    vcno = Column(String(2), nullable=False)   # 选项编号
    vctext = Column(Text, nullable=False)      # 选项描述
    vcnext = Column(String(2))                 # 选项对应下一题，可空，默认为VOid对应VOno+1
    vctype = Column(Integer)                   # 选项类型 是否需要增加文本框{1200: 不需要，1201：需要}
    void = Column(String(64))                  # 问题id


class Votenotes(Base):
    __tablename__ = "Votenotes"
    vnid = Column(String(64), primary_key=True)
    vsid = Column(String(64))
    openid = Column(String(200))    # 用户ID
    vntime = Column(String(14))  # 答题时间


class VoteResult(Base):
    __tablename__ = "VoteResult"
    vrid = Column(String(64), primary_key=True)
    vnid = Column(String(64))     # 答题记录id
    void = Column(String(64))     # 问题id
    vrchoice = Column(String(16))  # 选项
    vrabo = Column(Text)          # 详情： 填空和其他用

class AIR_HWYS_DZJJD(Base):
    __tablename__ = "AIR_HWYS_DZJJD"
    jjd_id = Column(String(40), primary_key=True)
    jcno = Column(String(20))                       # 进仓单号
    rkd_flag = Column(String(10))                   # 入库单交接标识
    jd_flag = Column(String(40))                    # 鉴定标识
    ddl_flag = Column(String(10))                   # 是否打代理标识
    state_goods = Column(String(20))                # 货物状态
    temperature = Column(String(40))                # 温度区间
    tc_num = Column(String(40))                     # 干冰用量
    dtp = Column(String(40))                        # 打托盘
    tp_mass = Column(String(40))                    # 托盘材质
    tp_size = Column(String(40))                    # 托盘尺寸
    in_mark = Column(String(100))                   # 内唛头
    ybzbl_flag = Column(String(10))                 # 原包装是否保留标识
    goods_file = Column(String(10))                 # 随货文件
    nbzsm = Column(String(2000))                    # 内包装说明
    kh = Column(String(10))                         # 客货机
    sbxx = Column(String(1000))                     # 申报信息
    kf_bz = Column(String(2000))                    # 仓库要求
    kf_ry = Column(String(40))                      # 库房人员
    kfqr_date = Column(DATE)                        # 库房确认时间
    hc_ry = Column(String(40))                      # 货场人员
    hcqr_date = Column(DATE)                        # 货场确认时间
    out_mark = Column(String(100))                  # 外唛头
    bzpm = Column(String(1000))                     # 包装品名
    ice_flag = Column(String(10))                   # 加冰处理
    gb_flag = Column(String(10))                    # 加干冰标识
    gb_num = Column(String(40))                     # 干冰用量
    lb_flag = Column(String(10))                    # 加蓝冰标识
    lb_num = Column(String(40))                     # 蓝冰用量
    sjwj_flag = Column(String(10))                  # 随机文件
    hc_bz = Column(String(2000))                    # 货场要求
    creat_time = Column(DATE)                       # 创建时间
    ungoods_flag = Column(String(10))               # 无货转库房标识

class AIR_HWYS_QRD(Base):
    __tablename__ = "AIR_HWYS_QRD"
    id = Column(String(200), primary_key=True)
    ydno = Column(String(20))                       # 运单号
    jcno = Column(String(200))                      # 进仓号
    title = Column(String(500))                     # 发票抬头
    rate = Column(String(20))                       # 汇率
    doc = Column(String(200))                       # 费用种类
    curr = Column(String(200))                      # 单价
    currcode = Column(String(50))                   # 币种
    amount = Column(String(100))                    # 数量
    byzd1 = Column(String(500))                     # 账单或成本的标识，空位账单，1为成本
    byzd2 = Column(String(500))                     # 成本录入人
    byzd3 = Column(String(500))                     # 备用字段
    createtime = Column(DATE)                       # 填写时间
    fkdw = Column(String(2000))                     # 付款单位
    hxno = Column(String(2000))                     # 发票号

class D_CHARGE_COMPANY(Base):
    __tablename__ = "D_CHARGE_COMPANY"
    id = Column(String(200), primary_key=True)
    company = Column(String(200))                   # 公司
    createtime = Column(DATE)                       # 创建时间
    code = Column(String(50))                       # 简码
    create_user = Column(String(40))                # 填写人
    pay_month = Column(String(10))                  # 付款月份
    pay_day = Column(String(10))                    # 付款日

class D_CHARGE_TYPE(Base):
    __tablename__ = "D_CHARGE_TYPE"
    charge_code = Column(String(20), primary_key=True)                # 简码
    charge_cname = Column(String(50))               # 费用种类名称
    charge_name = Column(String(50))
    remark = Column(String(100))                    # 备注
    create_by = Column(String(20))                  # 创建人
    create_date = Column(DATE)                      # 创建时间
    update_by = Column(String(20))                  # 更改人
    update_date = Column(DATE)                      # 更改时间
    d_price = Column(String(100))                   # 单价
    d_charge_id = Column(String(40))                # 主键id
    charge_group_id = Column(String(40))            # 父类id
    charge_type = Column(String(100))               # 规格

class AIR_HWYS_CKMXD(Base):
    __tablename__ = "AIR_HWYS_CKMXD"
    list_id = Column(String(40), primary_key=True)  # 仓库明细单id
    jcno = Column(String(20))                       # 进仓编号
    hwpm = Column(String(2000))                     # 货物品名
    warehouse_address = Column(String(100))         # 货物存放地
    enter_time = Column(DATE)                       # 进仓时间
    goods_quantity = Column(String(20))             # 件数
    delivery_unit = Column(String(200))             # 送货单位
    goods_weight = Column(String(20))               # 重量
    contact_phone = Column(String(20))              # 联系方式
    originator_phone = Column(String(20))           # 始发方电话
    receiver_name = Column(String(50))              # 接货人
    cargo_size = Column(String(100))                # 货物尺寸
    salesman = Column(String(20))                   # 业务员
    client_name = Column(String(50))                # 客户名称
    shipping_mark = Column(String(500))             # 唛头
    remark = Column(String(2000))                   # 备注
    store_keeper = Column(String(50))               # 库管
    consignee = Column(String(50))                  # 提货人
    pickup_date = Column(DATE)                      # 提货日期
    creator = Column(String(50))                    # 创建人
    create_time = Column(DATE)                      # 创建时间
    photo_head = Column(String(10))                 # 照片批次

class AIR_HWYS_PHOTO_HEAD(Base):
    __tablename__ = "AIR_HWYS_PHOTO_HEAD"
    id = Column(String(100), primary_key=True)
    photohead = Column(String(200))
    jcno = Column(String(100))
    type = Column(String(20))
    createtime = Column(DATE)
    czr = Column(String(100))
    photocount = Column(NUMBER)

class AIR_HWYS_OUTWAREHOUSE(Base):
    __tablename__ = "AIR_HWYS_OUTWAREHOUSE"
    id = Column(String(36), primary_key=True)
    ydno = Column(String(32))                       # 运单号
    submitter = Column(String(16))                  # 提交人
    submit_time = Column(DATE)                      # 提交时间
    create_time = Column(DATE)                      # 创建时间

class AIR_HWYS_INGOODYARD(Base):
    __tablename__ = "AIR_HWYS_INGOODYARD"
    id = Column(String(36), primary_key=True)
    ydno = Column(String(32))                       # 运单号
    submitter = Column(String(16))                  # 提交人
    submit_time = Column(DATE)                      # 提交时间
    create_time = Column(DATE)                      # 创建时间

class AIR_HWYS_DGD_UPLOAD(Base):
    __tablename__ = "AIR_HWYS_DGD_UPLOAD"
    id = Column(String(100), primary_key=True)
    jcno = Column(String(40))                       # 进仓单号
    ydno = Column(String(40))                       # 运单号
    file_type = Column(String(100))                 # 种类：申报单/包装明细/鉴定文件
    file_url = Column(String(200))                  # 存储路径
    create_time = Column(DATE)                      # 文件上传时间
    create_user = Column(String(100))               # 文件上传人
    file_name = Column(String(100))                 # 文件名称
    file_remark = Column(String(100))               # 文件备注信息

class AIR_HWYS_DGD_UPLOAD_BAK(Base):
    __tablename__ = "AIR_HWYS_DGD_UPLOAD_BAK"
    id = Column(String(100), primary_key=True)
    jcno = Column(String(40))                       # 进仓单号
    ydno = Column(String(40))                       # 运单号
    file_type = Column(String(100))                 # 种类：申报单/包装明细/鉴定文件
    file_url = Column(String(200))                  # 存储路径
    upload_create_time = Column(DATE)               # 文件上传时间
    upload_create_user = Column(String(100))        # 文件上传人
    file_name = Column(String(100))                 # 文件名称
    file_remark = Column(String(100))               # 文件备注信息
    upload_id = Column(String(100))                 # upload关联id
    delete_time = Column(DATE)                      # 文件删除时间
    delete_user = Column(String(100))               # 文件删除人

class AIR_HWYS_PACK_ROYALTY(Base):
    __tablename__ = "AIR_HWYS_PACK_ROYALTY"
    id = Column(String(200), primary_key=True)
    jcno = Column(String(20))                       # 进仓单号
    packer_leader = Column(String(40))              # 包装负责热
    packer = Column(String(40))                     # 包装人员
    royalty_rate = Column(String(20))               # 提成比例
    create_date = Column(DATE)                      # 创建时间
    create_user = Column(String(40))                # 创建者
    packer_confrim = Column(String(20))             # 包装人员确认标识
    packer_ok = Column(String(20))                  # 包装人员包装宝成标识

class AIR_HWYS_ENQUIRY(Base):
    __tablename__ = "AIR_HWYS_ENQUIRY"
    id = Column(String(200), primary_key=True)
    departure = Column(String(50))                  # 起运地
    destination = Column(String(50))                # 目的地
    company = Column(String(100))                   # 航空公司
    pwkh = Column(String(20))                       # 普货危品客机货机，GEN普货PAX危品客机CAO危品货机
    usetime = Column(String(100))                   # 有效期
    weight_m = Column(String(50))                   # M
    weight_m_custom = Column(String(50))            # M对应客户价格
    weight_n = Column(String(50))                   # N
    weight_n_custom = Column(String(50))            # N对应客户价格
    weight_q45 = Column(String(50))                 # Q45
    weight_q45_custom = Column(String(50))          # Q45对应客户价格
    weight_q100 = Column(String(50))                # Q100
    weight_q100_custom = Column(String(50))         # Q100对应客户价格
    weight_q300 = Column(String(50))                # Q300
    weight_q300_custom = Column(String(50))         # Q300对应客户价格
    weight_q500 = Column(String(50))                # Q500
    weight_q500_custom = Column(String(50))         # Q500对应客户价格
    weight_q1000 = Column(String(50))               # Q1000
    weight_q1000_custom = Column(String(50))        # Q1000对应客户价格
    gtyt = Column(String(50))                       # 固体液体
    fuel = Column(String(50))                       # 燃油费用
    fuel_min = Column(String(50))                   # 燃油费用最低
    safe = Column(String(50))                       # 安全费用
    safe_min = Column(String(50))                   # 安全费用最低
    awb = Column(String(50))                        # awb
    attach = Column(String(50))                     # 附加费用
    attach_min = Column(String(50))                 # 附加费用最低
    remarks = Column(String(2000))                  # 备注

class D_ACCOUNTS(Base):
    __tablename__ = "D_ACCOUNTS"
    id = Column(NUMBER(10), primary_key=True)
    accounts_code = Column(String(20))              # 公司code
    accounts_name = Column(String(100))             # 公司名称
    b_airway = Column(NUMBER(10))                   # 需要判断值为“1”

class D_PORT(Base):
    __tablename__ = "D_PORT"
    port_code = Column(String(20), primary_key=True)# 目的地code
    port_cname = Column(String(50))                 # 目的地名称
    port_aircode = Column(String(20))               # 需要判断非空

if __name__ == "__main__":
    Base.metadata.create_all(mysql_engine)