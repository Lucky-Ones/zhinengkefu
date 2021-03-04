# -*- coding:utf-8 -*-
"""
======================
author : 豪哥
@time:2021/3/4:17:02
======================
"""
import pip
from subprocess import call
from pip._internal.utils.misc import get_installed_distributions
from subprocess import call
from time import sleep

for dist in get_installed_distributions():
    # 执行后，pip默认为Python3版本
    # 双版本下需要更新Python2版本的包，使用py2运行，并将pip修改成pip2
    call("pip install --upgrade " + dist.project_name, shell=True)

