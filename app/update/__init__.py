#-*- coding:utf-8 -*-
from flask import Blueprint
update=Blueprint('update',__name__)
from . import views,services