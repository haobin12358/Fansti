# -*- coding: utf-8 -*-
from flask_restful import Resource

from Fansti.config.response import APIS_WRONG
from Fansti.control.Cpay import CPay


class FSpay(Resource):
    def __init__(self):
        print('fspqy')
        self.cpay = CPay()

    def post(self, pay):
        print(pay)
        apis = {
            'pay_service': self.cpay.pay_service,
            'pay_notify': self.cpay.pay_notify
        }
        if pay not in apis:
            return APIS_WRONG
        return apis[pay]()

    def get(self, pay):
        apis = {
            'pay_hitory': self.cpay.pay_hitory
        }
        if pay not in apis:
            return APIS_WRONG
        return apis[pay]()