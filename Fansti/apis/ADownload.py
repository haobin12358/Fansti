# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from flask import send_from_directory

class ADownload(Resource):

    def get(self, jcno, jctype):
        return send_from_directory("E:\\fstfile\\photo\\{0}\\{1}\\".format(jcno, jctype), "{0}.zip".format(jctype), as_attachment=True)