# *- coding:utf8 *-
from flask import Flask
import flask_restful
from Fansti.apis.Ascrapy import FSscrapy
from Fansti.apis.AUsers import FSUser
from Fansti.apis.AGoods import FSGoods
from Fansti.apis.AOther import FSother
from Fansti.apis.AReds import FSRed
from Fansti.apis.ANews import FSNews
from Fansti.apis.AVotes import FSVotes

fansti = Flask(__name__)
api = flask_restful.Api(fansti)
api.add_resource(FSscrapy, "/fansti/scrapy/<string:scrapy>")
api.add_resource(FSUser, "/fansti/users/<string:users>")
api.add_resource(FSGoods, "/fansti/goods/<string:goods>")
api.add_resource(FSother, "/fansti/other/<string:other>")
api.add_resource(FSRed, "/fansti/reds/<string:reds>")
api.add_resource(FSNews, "/fansti/news/<string:news>")
api.add_resource(FSVotes, "/fansti/votes/<string:votes>")

@fansti.route("/")
def index():
    return "<html><body>Hello world</body></html>"


if __name__ == '__main__':
    fansti.run('0.0.0.0', 7444, debug=True)