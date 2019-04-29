# *- coding:utf8 *-
# 小程序id和secret
APP_ID = "wxad55d967c5abf395"
APP_SECRET_KEY = "ba77eaa590f149b9d444eb44cdcd0a65"

# 商家id和商家key
# mch_id = "1505464141"
# mch_key = "8ecWB0VuVAtwqnQsAG0FAdjDlhZWmY88"

mch_id = "1495984842"
mch_key = "8ecWB0VuVAtwqnQsAG0FAdjDlhZWmY88"
import os
base_dir = os.path.abspath(os.path.dirname(__file__))

# 图片存储地址
LinuxRoot = "/opt/"
LinuxImgs = "imgs/Fansti"
WindowsRoot = "E:/fstfile/photo"
WindowsImag = 'photo'

# url
ip = "https://fstwechat.com/"
# ip = "http://120.79.182.43:7443/"

# 服务器ip地址
NETWORK_IP = "123.207.97.185"

# 模板存放地址

LinuxTMP = "/tmp"
WindowsTMP = "D:\\template"
YDFILEROOT = r'E:\fstfile\uploadfile'

# AIRLINEDIR = "airline"
template_type_dir = {
    "AIRLINE": "airline",
    "DGR": "dgr",
    "TACT": 'tact',
}

# config路径
# FANSTICONFIG = "./fansticonfig.ini"
FANSTICONFIG = "../Fansti/Fansti/fansticonfig.ini"
