#-*- coding:utf-8 -*-
from .. import make_error,make_success
from . import select
from .services import *
from flask import jsonify
from MySQL import get_connection
from flask import jsonify,make_response

#训练
from gensim import corpora, models, similarities
import jieba

import xlrd
from MySQL import get_connection
from  flask import request
from flask import render_template,redirect,request,url_for,jsonify,send_from_directory,abort,send_file
from flask import Flask,make_response
import pymysql,json,os
import time
import time
conn = get_connection()
cur = conn.cursor()


sql1 = """SELECT problem,trueProblem FROM problem """
cur.execute(sql1)
results1 = cur.fetchall()
# print(results1)
rows1 = []
aa=[]
for i in results1:
    rows1.append(i[0])
    aa.append(i[1])
# print(rows1)
# print(aa)

d = dict(zip(rows1, aa))





# 输入文本集和搜索问题
texts1 = rows1
# keyword = input('输入问题')
# 1、将 文本集 生成  分词列表
texts = []
for text in texts1:
    with open("out/qu.txt", 'r',encoding='gbk') as cf:  # （去掉去停词）
        docs = cf.readlines()
        for line in docs:
            line = line.strip('\n')
            text = text.replace(line, '')
    #print(text)
    texts.append(jieba.lcut(text))
# print(texts)
# 2、基于文本集建立  词典  ，并提取词典特征数
dictionary = corpora.Dictionary(texts)
feature_cnt = len(dictionary.token2id)
# 3、基于词典，将  分词列表集  转换成  稀疏向量集  ，称作  语料库
corpus = []
for text in texts:
    corpus.append(dictionary.doc2bow(text))
# 4、使用   TF-IDF   处理语料库
tfidf = models.TfidfModel(corpus)
# 6、对   稀疏向量集  建立   索引
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_cnt)
index.save('index/index.index')  # 保存索引

def a1(words):
    keyword = words
    # 用  词典  把  搜索词   也转换为  稀疏向量
    kw_vector = dictionary.doc2bow(jieba.lcut(keyword))
    # 相似度计算
    index = similarities.MatrixSimilarity.load('index/index.index')  # 读取语料库索引
    sim = index[tfidf[kw_vector]]
    a = {}
    for i, text in enumerate(sim):
        a[i] = text
    # print(a)
    list1 = sorted(a.items(), key=lambda x: x[1], reverse=True)
    # print(list1[0][0])
    a = '匹配问题:\n'
    b = '相似度:\n'
    cc=[]
    dd=[]
    j = 0
    repeat = []  # 去掉重复
    for i in range(100):
        if i == 0:
            repeat.append(d[texts1[list1[i][0]]])
            # print(j + 1, '.', d[texts1[list1[i][0]]], '+', texts1[list1[i][0]], '相似度:', list1[i][1])
            a = a + str(j + 1) + '.' + d[texts1[list1[i][0]]] + '\n'
            b = b + str(j + 1) + '.' + '相似度:' + str(list1[i][1]) + '\n'
            cc.append(d[texts1[list1[i][0]]])
            dd.append(list1[i][1])
            j = j + 1
        else:
            if d[texts1[list1[i][0]]] in repeat:  # 去掉重复
                pass
            else:
                repeat.append(d[texts1[list1[i][0]]])
                # print(j + 1, '.', d[texts1[list1[i][0]]], '+', texts1[list1[i][0]], '相似度:', list1[i][1])
                a = a + str(j + 1) + '.' + d[texts1[list1[i][0]]] + '\n'
                b = b + str(j + 1) + '.' + '相似度:' + str(list1[i][1]) + '\n'
                cc.append(d[texts1[list1[i][0]]])
                dd.append(list1[i][1])
                j = j + 1
                if j == 5:
                    break
    # print(a)
    return cc, dd
# 训练
cur.close()
conn.close()


@select.route('problem', methods=['POST', 'GET'])#查找问题详细信息
def select_problem():
    if problem():
        data = problem()
        return data
    else:
        data = json.dumps(make_error(), ensure_ascii=False)
        return data


@select.route('ask', methods=['POST', 'GET'])#用户问客服
def select_ask():
    a = request.get_data()
    a = str(a, 'utf-8')
    a = json.loads(a)
    print(a)
    problem = a["problem"]
    a, b = a1(problem)
    t = time.strftime("%H:%M:%S", time.localtime())
    if b[0]<0.4:
        data = {'problem': "相似度过低","oldProblem":problem,'time': t,'judge': "0"}
    else:
        data = {'problem': a,"oldProblem":problem,'time': t,'judge': "1"}
    data = json.dumps(data, ensure_ascii=False)
    return data


@select.route('concreteClass', methods=['POST', 'GET'])#查找类别
def select_concreteClass():
    if concreteClass():
        data = concreteClass()
        return data
    else:
        data = json.dumps(make_error(), ensure_ascii=False)
        return data

@select.route('useful', methods=['POST', 'GET'])#查找类别
def select_useful():
    if useful():
        data = useful()
        return data
    else:
        data = json.dumps(make_error(), ensure_ascii=False)
        return data



@select.route('userProblem', methods=['POST', 'GET'])#查找类别
def select_userProblem():
    if userProblem():
        data = userProblem()
        return data
    else:
        data = json.dumps(make_error(), ensure_ascii=False)
        return data


@select.route('category', methods=['POST', 'GET'])#查找类别
def select_category():
    if category():
        data = category()
        return data
    else:
        data = json.dumps(make_error(), ensure_ascii=False)
        return data

@select.route('classification', methods=['POST', 'GET'])#查找类别
def select_classification():
    if classification():
        data = classification()
        return data
    else:
        data = json.dumps(make_error(), ensure_ascii=False)
        return data

@select.route('/img/<string:filename>', methods=['GET',"POST"])  #分类图片
def show_photo(filename):
    if request.method == 'GET'or request.method == 'POST':
        print(filename)
        if filename is None:
            pass
        else:
            print('/static/gif/%s' % filename)
            image_data = open(os.path.join('static/gif/%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass



@select.route('barrage', methods=['POST', 'GET'])#弹幕
def select_barrage():
    if barrage():
        data = barrage()
        return data
    else:
        data = json.dumps(make_error(), ensure_ascii=False)
        return data

@select.route('red', methods=['POST', 'GET'])#弹幕
def select_red():
    if red():
        data = red()
        return data
    else:
        data = json.dumps(make_error(), ensure_ascii=False)
        return data


@select.route('information', methods=['POST', 'GET']) #查询个人信息
def select_information():
    if information():
        data = information()
        return data
    else:
        data = json.dumps(make_error(), ensure_ascii=False)
        return data

