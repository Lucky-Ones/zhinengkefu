#-*- coding:utf-8 -*-
from MySQL import get_connection
from  flask import request
from flask import render_template,redirect,request,url_for,jsonify,send_from_directory,abort,send_file
from flask import Flask,make_response
import pymysql,json,os,requests

#
# def Login():
#     if request.method == 'POST':
#         conn = get_connection()
#         cur = conn.cursor()
#         a = request.get_data()
#         a = str(a, 'utf-8')
#         dict1 = json.loads(a)
#         Username = dict1['Username']
#         Password = dict1['Password']
#         sql1 = "select * from user WHERE Username = '%s' " % (Username)
#         cur.execute(sql1)
#         results1 = cur.fetchall()
#         if results1:
#             sql2 = "select * from user WHERE Username = '%s'and Password = '%s' " % (Username, Password)
#             cur.execute(sql2)
#             results2 = cur.fetchall()
#             cur.close()
#             conn.close()
#             if results2:
#                 return ('1')
#             else:
#                 return ('0')
#         else:
#             cur.close()
#             conn.close()
#             return ('用户不存在')
#     else:
#         return None
#
# def Change():
#     if request.method == 'POST':
#         conn = get_connection()
#         cur = conn.cursor()
#         a = request.get_data()
#         a = str(a, 'utf-8')
#         dict1 = json.loads(a)
#         Username = dict1['Username']
#         OldPassword = dict1['OldPassword']
#         NewPassword = dict1['NewPassword']
#         NewPassword2 = dict1['NewPassword2']
#         if NewPassword != NewPassword2:
#             return ('两次输入密码不一样')
#
#         sql1 = "select * from user WHERE Username = '%s' and Password = '%s' " % (Username, OldPassword)
#         cur.execute(sql1)
#         results1 = cur.fetchall()
#         if results1:
#             sql2 = """UPDATE user set Password = '%s' where Username = '%s'AND Password = '%s'""" % (NewPassword, Username, OldPassword)
#             try:
#                 cur.execute(sql2)
#                 # 提交
#                 conn.commit()
#             except Exception as e:
#                 # 错误回滚
#                 conn.rollback()
#                 return ('修改失败')
#             finally:
#                 cur.close()
#                 conn.close()
#                 return ('修改成功')
#         else:
#             cur.close()
#             conn.close()
#             return ('密码错误')
#     else:
#         return None



def login_():
    if request.method == 'POST'or request.method == 'GET':
        conn = get_connection()
        cur = conn.cursor()
        a = request.get_data()
        a = str(a, 'utf-8')
        a = json.loads(a)
        # print(a)

        code = a["code"]
        appid = a["appid"]
        secret = a["secret"]

        # https://api.weixin.qq.com/sns/jscode2session?appid=你的appid&secret=你的secret&grant_type=authorization_code&js_code=登录code
        url = "https://api.weixin.qq.com/sns/jscode2session" \
              "?appid=%s&secret=%s&grant_type=authorization_code&js_code=%s"%(appid,secret,code)
        def WWWrequest():
            content = requests.get(url)
            # print(content.text)
            c = content.text
            # c = str(content, 'utf-8')
            c = json.loads(c)
            return c
        c = WWWrequest()
        try:
            while 1:
                errcode = c["errcode"]
                errmsg = c["errmsg"]
                if errcode == "-1":
                    c = WWWrequest()
                else:
                    break
            if errcode == 40013 or errcode == 40163:
                # print(errmsg)
                data = {'errmsg1': errmsg, "errmsg": "code无效", "judge": "0"}
                data = json.dumps(data, ensure_ascii=False)
                return data
        except KeyError:
            pass

        if 1:
            # openid和sessionid
            session_key = c["session_key"]
            openid = c["openid"]
            # unionid = c["unionid"]
            sql1 = """insert into `user` (userID) values('%s') """ % (openid)
            try:
                cur.execute(sql1)
                # 提交
                conn.commit()
            except Exception as e:
                # 错误回滚
                conn.rollback()
                aaaa = '已经注册'
            sql1 = """UPDATE `user` SET `session_key` = '%s' where userID = '%s'""" %( session_key,openid)
            print("sql1=%s"%sql1)

            try:
                cur.execute(sql1)
                # 提交
                conn.commit()
            except Exception as e:
                # 错误回滚
                conn.rollback()
                return ('修改失败')
            zzz = []
            data = {'openid': openid, "session_key": session_key, "judge": "1"}
            data = json.dumps(data, ensure_ascii=False)
            cur.close()
            conn.close()
            return data
    else:
        return None


