#-*- coding:utf-8 -*-
from MySQL import get_connection
from  flask import request
from flask import render_template,redirect,request,url_for,jsonify,send_from_directory,abort,send_file
from flask import Flask,make_response
import pymysql,json,os



def enquire():#提问
    if request.method == 'POST':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        userID = a["userID"]
        userProblem = a["userProblem"]
        userAnswer = "暂时无解答"
        print(userProblem)
        sql1 = """insert into enquire (userID,userProblem,userAnswer,sign) values('%s','%s','%s',"%s") """ % (userID, userProblem,userAnswer,0)
        print()

        print(sql1)
        print()

        try:
            cur.execute(sql1)
            # 提交
            conn.commit()
        except Exception as e:
            # 错误回滚
            conn.rollback()
            return ('修改失败')
        data = {'judge': '1'}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None


def information():   #插入个人信息
    if request.method == 'POST'or request.method == 'GET':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        print("--------------------------")

        print(a)
        print("--------------------------")

        openid = a["openid"]
        username = a["username"]
        portrait = a["portrait"]
        sex = a["sex"]
        grade = a["grade"]

        if sex=="2" or sex==2:
            sex = "女"
        elif sex=="1" or sex==1:
            sex = "男"
        elif   sex=="0"or sex==0:
            sex = "未知"
        zzz=[]
        sql1 = """insert into `user` (userID,username,grade,sex,portrait) values('%s','%s','%s','%s','%s') 
        """ % (openid, username, grade,sex,portrait)
        print(sql1)
        # cur.execute(sql1)
        # # 提交
        # conn.commit()
        try:
            cur.execute(sql1)
            # 提交
            conn.commit()
        except Exception as e:
            # 错误回滚
            conn.rollback()
            return ('已经保存过这个人的信息，修改请访问update/information 接口')
        data = {"openid": openid,"username": username,"portrait": portrait,"sex": sex,"grade": grade,"judge": "1"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()

        return data
    else:
        return None
