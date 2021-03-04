#-*- coding:utf-8 -*-
import time
from MySQL import get_connection
from  flask import request
from flask import render_template,redirect,request,url_for,jsonify,send_from_directory,abort,send_file
from flask import Flask,make_response
import pymysql,json,os
import time,random

def randomcolor():#随机字体颜色   #89CF59    #C69DF7
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color



def problem():#查找问题详细信息
    if request.method == 'POST':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        print(a)
        problem = a["problem"]
        zzz=[]
        sql1 = """SELECT * FROM `answer` WHERE trueProblem = "%s" """  % (problem)
        cur.execute(sql1)
        results1 = cur.fetchall()
        # 提交
        for row in results1:
            date = {"problemID": str(row[0]), "trueProblem": row[1], "answer": row[2],
                    "good": str(row[4]),"bad": str(row[4])}
            zzz.append(date)
        data = {'data': zzz,"judge": "1"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None

def concreteClass():#查找分类问题
    if request.method == 'POST':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        page = a["page"]
        categoryID = a["category"]
        classification = a["classification"]
        zzz=[]
        sql1 = """SELECT trueProblem FROM `answer` WHERE category = "%s" and classification = "%s" limit %s,10"""  % (categoryID,classification,page)
        cur.execute(sql1)
        results1 = cur.fetchall()
        # 提交
        for row in results1:
            date = {"problem": row[0]}
            zzz.append(date)
        data = {'data': zzz,"judge": "1"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None



def useful():#查找对我有用
    if request.method == 'POST':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        page = a["page"]
        userID = a["userID"]
        zzz=[]
        sql1 = """SELECT trueProblem,answer FROM useful,answer WHERE  useful.userID = "%s" 
        and useful.problemID = answer.problemID  limit %s,10"""  % (userID,page)
        cur.execute(sql1)
        results1 = cur.fetchall()
        # 提交
        for row in results1:
            date = {"trueProble": row[0],"answer": row[1]}
            zzz.append(date)
        data = {'data': zzz,"judge": "1"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None





def userProblem():#查找我的提问
    if request.method == 'POST':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        print(".......")
        print(a)
        print(".......")
        a = str(a, 'utf-8')
        a = json.loads(a)
        userID = a["userID"]
        page = a["page"]
        zzz=[]
        sql1 = """SELECT * FROM enquire WHERE  userID = "%s"  limit %s,10"""  % (userID,page)
        cur.execute(sql1)
        results1 = cur.fetchall()
        # 提交
        for row in results1:
            date = {"enquireID": row[0],"userProblem": row[2],"userAnswer": row[3]}
            zzz.append(date)
        data = {'data': zzz,"judge": "1"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None


def category():  # 查找8个类别
    if request.method == 'POST'or request.method == 'GET':
        conn = get_connection()
        cur = conn.cursor()
        zzz = []
        sql1 = """SELECT * FROM classaaa """
        cur.execute(sql1)
        results1 = cur.fetchall()
        # 提交
        for row in results1:
            date = {"ID": row[0],"category": row[1],"url": row[2]}
            zzz.append(date)
        data = {'data': zzz, "judge": "1"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None


def classification():  # 查找3个类别
    if request.method == 'POST'or request.method == 'GET':
        conn = get_connection()
        cur = conn.cursor()
        zzz = []
        sql1 = """SELECT * FROM classbbb """
        cur.execute(sql1)
        results1 = cur.fetchall()
        # 提交
        for row in results1:
            date = {"ID": row[0],"classification": row[1]}
            zzz.append(date)
        data = {'data': zzz, "judge": "1"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None

def barrage():#弹幕
    if request.method == 'POST'or request.method == 'GET':
        conn = get_connection()
        cur = conn.cursor()
        zzz=[]
        sql1 = """SELECT * FROM `answer` ORDER BY RAND() LIMIT 20 """
        cur.execute(sql1)
        results1 = cur.fetchall()
        # 提交
        resultList = random.sample(range(0, 80), 20);  # 表示从[A,B]间随机生成N个数，结果以列表返回
        i = 0
        problem={}
        for row in results1:
            date = {"problemID": str(row[0]), "trueProblem": row[1], "duration": random.randint(0, 10)
                , "top":resultList[i], "color": randomcolor()}
            i = i+1
            zzz.append(date)
        data = {'data': zzz,"judge": "1"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None




def red():#红点
    if request.method == 'POST'or request.method == 'GET':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        userID = a["userID"]
        zzz=[]
        sql1 = """SELECT * FROM `enquire` where  sign = 0 and userID = "%s"  """ %(userID)
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
            data = {'enquireID': bb,"newAnswer": "true"}
        else:
            data = {'enquireID': bb,"newAnswer": "false"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None




def information():   #查询个人信息
    if request.method == 'POST'or request.method == 'GET':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        openid = a["openid"]
        sql1 = """SELECT * FROM `user` where  userID = "%s"  """ % (openid)
        cur.execute(sql1)
        results1 = cur.fetchall()
        data1=0
        print("==========")
        print(results1)
        print("==========")

        for row in results1:
            data1 = {"openid": str(row[0]), "username": row[1], "portrait":row[6], "sex":row[4], "grade": row[3]}
        data = {"data":data1,"judge": "1"}
        data = json.dumps(data, ensure_ascii=False)
        cur.close()
        conn.close()
        return data
    else:
        return None






