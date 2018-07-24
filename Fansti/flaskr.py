# *- coding:utf8 *-
from flask import Flask
import flask_restful
from Fansti.apis.Ascrapy import FSscrapy

fansti = Flask(__name__)
api = flask_restful.Api(fansti)
api.add_resource(FSscrapy, "/fansti/scrapy/<string:scrapy>")

if __name__ == '__main__':
    fansti.run('0.0.0.0', 7444, debug=True)