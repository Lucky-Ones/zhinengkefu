#-*- coding:utf-8 -*-

from flask import render_template,redirect,request,url_for,jsonify,send_from_directory,abort,send_file
from flask import Flask,make_response
import pymysql,json,os
from MySQL import get_connection


from gensim import corpora, models, similarities
import jieba
import tkinter
from tkinter import *
import xlrd
from MySQL import get_connection
from  flask import request
from flask import render_template,redirect,request,url_for,jsonify,send_from_directory,abort,send_file
from flask import Flask,make_response
import pymysql,json,os
import time

conn = get_connection()
cur = conn.cursor()

sql1 = """SELECT problem,trueProblem FROM problem """
cur.execute(sql1)
results1 = cur.fetchall()
print(results1)
rows1 = []
aa = []
for i in results1:
    rows1.append(i[0])
    aa.append(i[1])
print(rows1)
print(aa)

d = dict(zip(rows1, aa))

# 输入文本集和搜索问题
texts1 = rows1
# keyword = input('输入问题')
# 1、将 文本集 生成  分词列表
texts = []
for text in texts1:
    with open("out/qu.txt", 'r') as cf:  # （去掉去停词）
        docs = cf.readlines()
        for line in docs:
            line = line.strip('\n')
            text = text.replace(line, '')
    # print(text)
    texts.append(jieba.lcut(text))
print(texts)
# 2、基于文本集建立  词典  ，并提取词典特征数
dictionary = corpora.Dictionary(texts)
feature_cnt = len(dictionary.token2id)
# 3、基于词典，将  分词列表集  转换成  稀疏向量集  ，称作  语料库
corpus = []
for text in texts:
    corpus.append(dictionary.doc2bow(text))
print(corpus)
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
    print("list1list1list1list1")
    print(list1)
    print("list1list1list1list1")
    # print(list1[0][0])
    a = '匹配问题:\n'
    b = '相似度:\n'
    cc = []
    dd = []
    j = 0
    repeat = []  # 去掉重复
    for i in range(100):
        if i == 0:
            repeat.append(d[texts1[list1[i][0]]])
            print(j + 1, '.', d[texts1[list1[i][0]]], '+', texts1[list1[i][0]], '相似度:', list1[i][1])
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
                print(j + 1, '.', d[texts1[list1[i][0]]], '+', texts1[list1[i][0]], '相似度:', list1[i][1])
                a = a + str(j + 1) + '.' + d[texts1[list1[i][0]]] + '\n'
                b = b + str(j + 1) + '.' + '相似度:' + str(list1[i][1]) + '\n'
                cc.append(d[texts1[list1[i][0]]])
                dd.append(list1[i][1])
                j = j + 1
                if j == 5:
                    break
    # print(a)
    return cc, dd

app = Flask(__name__)



@app.route('/')
def hello_world():
    time_start = time.time()


    a, b = a1("证券转银行为什么转不了")
    print("============")
    print(a, b)
    time_end = time.time()
    print('time', time_end - time_start)
    return 'Hello World!'


if __name__ == '__main__':



    app.run()
