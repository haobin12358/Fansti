# *- coding:utf8 *-
from flask import Flask
import flask_restful
from Fansti.apis.Ascrapy import FSscrapy
from Fansti.apis.AUsers import FSUser
from Fansti.apis.AGoods import FSGoods

fansti = Flask(__name__)
api = flask_restful.Api(fansti)
api.add_resource(FSscrapy, "/fansti/scrapy/<string:scrapy>")
api.add_resource(FSUser, "/fansti/users/<string:users>")
api.add_resource(FSGoods, "/fansti/goods/<string:goods>")

if __name__ == '__main__':
    fansti.run('0.0.0.0', 7444, debug=True)