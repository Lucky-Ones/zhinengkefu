#-*- coding:utf-8 -*-
from MySQL import get_connection
from  flask import request
from flask import render_template,redirect,request,url_for,jsonify,send_from_directory,abort,send_file
from flask import Flask,make_response
import pymysql,json,os


def good():#有用，并且添加
    if request.method == 'POST':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        userID = a["userID"]
        judge = a["judge"]
        problemID = a["problemID"]
        sql3 = """SELECT good,bed FROM `answer` WHERE problemID = "%s" """ % (problemID)
        if judge == "1" or judge == 1:
            sql1 = """UPDATE answer SET `good` = `good` + 1 where problemID = %s"""  % problemID
            sql2 = """insert into useful (userID,problemID) values('%s','%s') """% (userID,problemID)
        elif judge == "0" or judge == 0:
            sql1 = """UPDATE answer SET `good` = `good` - 1  where problemID = %s""" % problemID
            sql2 = """delete from useful where userID = '%s'and  problemID = '%s'""" % (userID,problemID)
        try:
            cur.execute(sql1)
            cur.execute(sql2)
            # 提交
            conn.commit()
            cur.execute(sql3)
            results1 = cur.fetchall()
        except Exception as e:
            # 错误回滚
            conn.rollback()
            return ('修改失败')
        zzz=[]
        for row in results1:
            date = {"good": str(row[0]),"bad": str(row[1]),"judge": "1"}
            zzz.append(date)
        # data = {'data': zzz,"judge": "1"}
        data = json.dumps(date, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None

def bed():#无用
    if request.method == 'POST':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        problemID = a["problemID"]
        judge = a["judge"]
        print(judge)
        sql3 = """SELECT good,bed FROM `answer` WHERE problemID = "%s" """ % (problemID)
        if judge == "1" or judge ==1:
            sql1 = """UPDATE answer SET `bed` = `bed` + 1 where problemID = %s"""  % problemID
        elif judge == "0" or judge ==0:
            sql1 = """UPDATE answer SET `bed` = `bed` - 1  where problemID = %s""" % problemID

        try:
            cur.execute(sql1)
            # 提交
            conn.commit()
            cur.execute(sql3)
            results1 = cur.fetchall()
        except Exception as e:
            # 错误回滚
            conn.rollback()
            return ('修改失败')
        zzz = []
        for row in results1:
            date = {"good": str(row[0]), "bad": str(row[1]),"judge": "1"}
            zzz.append(date)
        # data = {'data': zzz,"judge": "1"}
        data = json.dumps(date, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None



def delRed():#红点
    if request.method == 'POST'or request.method == 'GET':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        problemID = a["problemID"]
        zzz=[]
        sql1 = """UPDATE answer SET `bed` = `bed` + 1 where problemID = %s""" % problemID

        cur.execute(sql1)
        results1 = cur.fetchall()
        # 提交
        aa = {}
        for row in results1:
            aa[row[0]]= row[3]
        print(aa)
        bb=[]
        for i in aa:
            if aa[i] != "暂时无解答":
                print(i)
                bb.append(i)
        print(bb)
        if bb:
            data = {'problemID': bb,"newAnswer": "true"}
        else:
            data = {'problemID': bb,"newAnswer": "false"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None

def delRed():#去掉红点
    if request.method == 'POST':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        enquireID = a["enquireID"].split(',')
        print(enquireID)
        for i in enquireID:
            print(i)
            sql1 = """UPDATE enquire SET `sign` = 1 where enquireID = %s"""  % i
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
        openid = a["openid"]
        username = a["username"]
        portrait = a["portrait"]
        sex = a["sex"]
        grade = a["grade"]
        print("update:%s"%a)
        if sex=="2" or sex==2:
            sex = "女"
        elif sex=="1" or sex==1:
            sex = "男"
        elif   sex=="0"or sex==0:
            sex = "未知"
        zzz=[]
        sql1 = """UPDATE `user` SET `username` = "%s",portrait="%s",sex="%s",grade="%s" where userID = "%s" """ \
               % (username,portrait,sex,grade,openid)
        print("sql1 = %s"%sql1)
        cur.execute(sql1)
        # 提交
        conn.commit()
        try:
            cur.execute(sql1)
            # 提交
            conn.commit()
        except Exception as e:
            # 错误回滚
            conn.rollback()
            return ('修改失败')
        data = {"openid": openid,"username": username,"portrait": portrait,"sex": sex,"grade": grade,"judge": "1"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None






