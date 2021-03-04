#-*- coding:utf-8 -*-
from .. import make_error,make_success
from . import update
from .services import *
from flask import jsonify
from MySQL import get_connection


@update.route('good', methods=['POST', 'GET'])#按ID查询
def update_good():
    data = good()
    return data

@update.route('bad', methods=['POST', 'GET'])#按ID查询
def update_bed():
    data = bed()
    return data


@update.route('delRed', methods=['POST', 'GET'])#按ID查询
def update_delRed():
    data = delRed()
    return data

@update.route('/information', methods=['POST', 'GET'])#登录
def update_information():
    data=information()
    return data








