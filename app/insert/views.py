#-*- coding:utf-8 -*-
from .. import make_error,make_success
from . import insert
from .services import *
from flask import jsonify
from MySQL import get_connection


@insert.route('enquire', methods=['POST', 'GET'])#按ID查询
def insert_enquire():
    data = enquire()
    return data

@insert.route('hello', methods=['POST', 'GET'])#按ID查询
def hello():
    return "hello world"



@insert.route('information', methods=['POST', 'GET'])#按ID查询
def insert_information():
    data = information()
    return data
