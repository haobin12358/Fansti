# *- coding:utf8 *-
from flask import Flask
import flask_restful
#from flask_cors import CORS

#from ManagerSystem.apis.AManager import MSManager
#from ManagerSystem.apis.AStocks import MSStocks
#from ManagerSystem.apis.AProducts import MSProduct
#from ManagerSystem.apis.AOrder import MSOrder
#from ManagerSystem.apis.ACotegory import MSCategory
#from ManagerSystem.apis.MSApproval import MSApproval
#from ManagerSystem.apis.AOther import AOther
#from ManagerSystem.apis.ACoupons import MSCoupons

from Fansti.apis.Ascrapy import FSscrapy
from Fansti.apis.AUsers import FSUser
from Fansti.apis.AGoods import FSGoods
from Fansti.apis.AOther import FSother
from Fansti.apis.AReds import FSRed
from Fansti.apis.ANews import FSNews

fansti = Flask(__name__)
#CORS(sg, resources=r'/*')
api = flask_restful.Api(fansti)
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求

#api.add_resource(MSManager, "/sharp/manager/user/<string:manager>")
#api.add_resource(MSStocks, "/sharp/manager/stock/<string:stock>")
#api.add_resource(MSProduct, "/sharp/manager/product/<string:product>")
#api.add_resource(MSOrder, "/sharp/manager/order/<string:order>")
#api.add_resource(MSCategory, "/sharp/manager/category/<string:category>")
#api.add_resource(MSApproval, "/sharp/manager/approval/<string:approval>")
#api.add_resource(AOther, "/sharp/manager/other/<string:other>")
#api.add_resource(MSCoupons, "/sharp/manager/card/<string:card>")

api.add_resource(FSscrapy, "/fansti/scrapy/<string:scrapy>")
api.add_resource(FSUser, "/fansti/users/<string:users>")
api.add_resource(FSGoods, "/fansti/goods/<string:goods>")
api.add_resource(FSother, "/fansti/other/<string:other>")
api.add_resource(FSRed, "/fansti/reds/<string:reds>")
api.add_resource(FSNews, "/fansti/news/<string:news>")

@fansti.route("/")
def index():
    return "<html><body>Hello world</body></html>"


'''
if __name__ == '__main__':
    sg.run('0.0.0.0', 443, debug=False, ssl_context=(
        "/etc/nginx/cert/1525609592348.pem"
    ))

'''
if __name__ == '__main__':
    fansti.run('0.0.0.0', 7443, debug=False)
# '''
