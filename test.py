#-*- coding:utf-8 -*-
# import time,random
# print(time.strftime("%H:%M:%S", time.localtime()))
# print(random.randint(12, 20)  )
# print(random.randint(12, 20)  )
# print(random.randint(12, 20)  )
# import random
# def randomcolor():
#     colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
#     color = ""
#     for i in range(6):
#         color += colorArr[random.randint(0,14)]
#     return "#"+color
#
# a = randomcolor()
# print(a)
#
# resultList=random.sample(range(0,81),81); #表示从[A,B]间随机生成N个数，结果以列表返回
# print(81 in resultList)
import requests,json

url = "https://api.weixin.qq.com/sns/jscode2session"
# content = requests.get(url)
# print(content.text)
code="081Hy3W02SzySV0swsU02rOdW02Hy3WB"
appid="wxaf6b32764de9c1e3"
secret="bcc08a9a33c001110c6677cf29167ed6"

url = "https://api.weixin.qq.com/sns/jscode2session" \
              "?appid=%s&secret=%s&grant_type=authorization_code&js_code=%s"%(appid,secret,code)
content = requests.get(url)
print(content.text)
# print(type(content.text))
a = content.text
# a = str(content.text, 'utf-8')
a = json.loads(a)
# openid和sessionid
print(a)
# errcode 1= a["errcode"]
# errmsg = a["errmsg"]
session_key = a["session_key"]
openid = a["openid"]
print(session_key)
print(openid)
# unionid = a["unionid"]
# print(a["errcode"])
# sessionid = a["sessionid"]