#-*- coding:utf-8 -*-
from flask import Flask
from .MySQL import DB
from flask_bootstrap import Bootstrap




def create_app():
    app=Flask(__name__)
    app.config.from_object('config')
    bootstrap = Bootstrap(app)
    from .login import login
    # from .control import control
    from .insert import insert
    from .select import select
    from .update import update
    app.register_blueprint(login,url_prefix='/login')
    app.register_blueprint(update,url_prefix='/update')
    app.register_blueprint(insert,url_prefix='/insert')
    app.register_blueprint(select,url_prefix='/select')
    return app
# def get_connection():
#     db = DB('47.106.168.80', 3306, 'root', 'pass', 'newbee')
#     return db.getConnection()
# def make_error(code=0, msg='请求失败', data=None):
#     return {
#         'error': {
#             'code': code,
#             'msg': msg,
#             'data': data
#         }
#     }
def make_success(code=1, msg='请求成功', data=None):
    return {
        'code': code,
        'msg': msg,
        'data': data
    }
def make_error(code=0, msg='请求失败', data=None):
    return {
        'error': '请求失败'
    }