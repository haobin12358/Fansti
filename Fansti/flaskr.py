# *- coding:utf8 *-
# from gevent import monkey
# monkey.patch_all(thread=False)
from flask import Flask, Blueprint
import flask_restful
from flask_cors import CORS

from Fansti.apis.APay import FSpay
from Fansti.apis.Ascrapy import FSscrapy
from Fansti.apis.AUsers import FSUser
from Fansti.apis.AGoods import FSGoods
from Fansti.apis.AOther import FSother
from Fansti.apis.AReds import FSRed
from Fansti.apis.ANews import FSNews
from Fansti.apis.AVotes import FSVotes
from Fansti.apis.AControl import FSControl
from Fansti.apis.ACommon import ACommon
from Fansti.apis.ADownload import ADownload
# # 处理高并发
# from gevent.pywsgi import WSGIServer
fansti = Flask(__name__)
# 跨域解决
CORS(fansti, resources=r'/*')
api = flask_restful.Api(fansti)
api.add_resource(FSscrapy, "/fansti/scrapy/<string:scrapy>")
api.add_resource(FSUser, "/fansti/users/<string:users>")
api.add_resource(FSGoods, "/fansti/goods/<string:goods>")
api.add_resource(FSother, "/fansti/other/<string:other>")
api.add_resource(FSRed, "/fansti/reds/<string:reds>")
api.add_resource(FSNews, "/fansti/news/<string:news>")
api.add_resource(FSVotes, "/fansti/votes/<string:votes>")
api.add_resource(FSpay, "/fansti/pay/<string:pay>")
api.add_resource(FSControl, "/fansti/control/<string:control>")
api.add_resource(ACommon, "/fansti/common/<string:common>")
# fansti.add_url_rule("/download/<string:jcno>/<string:jctype>")
v1 = Blueprint(__name__, 'v1', url_prefix='/fansti')
v1.add_url_rule('/download/<string:jcno>/<string:jctype>', view_func=ADownload.as_view('jcno'))
fansti.register_blueprint(v1)

@fansti.route("/download")
def index():
    return "<html><body>Hello world</body></html>"


# if __name__ == '__main__':
#     fansti.run('0.0.0.0', 8001, debug=True)
# WSGIServer(('127.0.0.1', 8001), fansti).serve_forever()

# from gevent import monkey
# from gevent.pywsgi import WSGIServer
# monkey.patch_all(thread=False)
# from flask  import Flask
# app = Flask(__name__)
#
# app.config.update(
#     DEBUG=True
# )
#
# @app.route('/asyn/1/', methods=['GET'])
# def test_asyn_one():
#     return "<html><body>Hello world</body></html>"
#
#
# @app.route('/test/', methods=['GET'])
# def test():
#     return 'hello test'
#
# if __name__ == "__main__":
#     # app.run()
#     http_server = WSGIServer(('', 5000), app)
#     http_server.serve_forever()