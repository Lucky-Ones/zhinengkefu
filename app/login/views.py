#-*- coding:utf-8 -*-
from .. import make_error,make_success
from . import login
from .services import *
from flask import jsonify
from MySQL import get_connection
# @login.route('/home', methods=['POST', 'GET'])#登录
# def alogin():
#     if Login():
#         data=Login()
#         return data
#     else:
#         data = json.dumps(make_error(), ensure_ascii=False)
#         return data
#
# @login.route('/change', methods=['POST', 'GET'])#登录
# def change():
#     data=Change()
#     return data
#
#
#

@login.route('/login', methods=['POST', 'GET'])#登录
def login_1():
    data=login_()
    return data









