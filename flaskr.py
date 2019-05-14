# *- coding:utf8 *-
from flask import Flask
import flask_restful
#from flask_cors import CORS

from Fansti.apis.APay import FSpay
from Fansti.apis.Ascrapy import FSscrapy
from Fansti.apis.AUsers import FSUser
from Fansti.apis.AGoods import FSGoods
from Fansti.apis.AOther import FSother
from Fansti.apis.AReds import FSRed
from Fansti.apis.ANews import FSNews
from Fansti.apis.AControl import FSControl
from Fansti.apis.ACommon import ACommon

fansti = Flask(__name__)
#CORS(sg, resources=r'/*')
api = flask_restful.Api(fansti)
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
api.add_resource(FSscrapy, "/fansti/scrapy/<string:scrapy>")
api.add_resource(FSUser, "/fansti/users/<string:users>")
api.add_resource(FSGoods, "/fansti/goods/<string:goods>")
api.add_resource(FSother, "/fansti/other/<string:other>")
api.add_resource(FSRed, "/fansti/reds/<string:reds>")
api.add_resource(FSNews, "/fansti/news/<string:news>")
api.add_resource(FSpay, "/fansti/pay/<string:pay>")
api.add_resource(FSControl, "/fansti/control/<string:control>")
api.add_resource(ACommon, "/fansti/common/<string:common>")

@fansti.route("/")
def index():
    return "<html><body>Hello world</body></html>"

if __name__ == '__main__':
    fansti.run('0.0.0.0', 7443, debug=False)
