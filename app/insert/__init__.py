#-*- coding:utf-8 -*-
from flask import Blueprint
insert=Blueprint('insert',__name__)
from . import views,services