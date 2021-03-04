
#-*- coding:utf-8 -*-
from flask import Blueprint
select=Blueprint('select',__name__)
from . import views,services