# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource

class ACommon(Resource):
    def __init__(self):
        self.title = "=========={0}=========="
        from Fansti.control.CGoods import CGoods
        self.common = CGoods()

    def get(self, common):
        apis = {
            "export_zip": self.common.export_zip
        }
        return apis
