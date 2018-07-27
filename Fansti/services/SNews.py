# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Fansti.models.model import WECHAT_NEWS
from Fansti.services.SBase import SBase, close_session

class SNews(SBase):

    @close_session
    def get_all(self, page_num, page_size):
        return self.session.query(WECHAT_NEWS.id, WECHAT_NEWS.news_title, WECHAT_NEWS.news_all,
                                  WECHAT_NEWS.news_picture, WECHAT_NEWS.news_from, WECHAT_NEWS.news_time)\
            .offset(page_size * (page_num - 1) + 1).limit(page_size).all()

    @close_session
    def get_message(self, id):
        return self.session.query(WECHAT_NEWS.id, WECHAT_NEWS.news_title, WECHAT_NEWS.news_all,
                                  WECHAT_NEWS.news_picture, WECHAT_NEWS.news_from, WECHAT_NEWS.news_time)\
            .filter_by(id=id).first()