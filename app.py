#-*- coding:utf-8 -*-

from flask import render_template,redirect,request,url_for,jsonify,send_from_directory,abort,send_file
from flask import Flask,make_response
import pymysql,json,os
from MySQL import get_connection

app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/login', methods=['POST', 'GET'])#登入
def login():
    conn = get_connection()
    cur = conn.cursor()
    a = request.get_data()
    a=str(a,'utf-8')
    dict1 = json.loads(a)
    telephone = dict1['telephone']
    password = dict1['password']
    sql1 = "select * from user WHERE telephone = '%s' " % (telephone)
    cur.execute(sql1)
    results1 = cur.fetchall()

    if results1:
        sql1 = "select * from user WHERE telephone = '%s'and password = '%s' "  % (telephone,password)
        cur.execute(sql1)
        results1 = cur.fetchall()
        cur.close()
        conn.close()
        if  results1:
            return ('1')
        else:
            return ('0')
    else:
        cur.close()
        conn.close()
        return ('2')

@app.route('/register', methods=['POST', 'GET'])#注册
def register():
    conn = get_connection()
    cur = conn.cursor()
    a = request.get_data()
    a = str(a, 'utf-8')
    a = json.loads(a)
    username = a["username"]
    password = a["password"]
    telephone = a["telephone"]
    portrait = a["portrait"]

    sql1 = """insert into user (username,password,telephone,portrait)
           values('%s','%s','%s','%s') """ % (username,password,telephone,1)
    try:
        cur.execute(sql1)
        # 提交
        conn.commit()
    except Exception as e:
        # 错误回滚
        conn.rollback()
        return ('电话号码已经注册')
    finally:
        cur.close()
        conn.close()
    return ('注册成功')


@app.route('/select/organize', methods=['POST', 'GET'])#按组查询
def select_organize():
    conn = get_connection()
    cur = conn.cursor()
    a = request.get_data()
    a = str(a, 'utf-8')
    a = json.loads(a)
    print(a)
    organize = a["organize"]

    zzz=[]
    sql1 = """SELECT * FROM student WHERE organize = %s """  % (organize)
    sql2 = """SELECT count(*) FROM student WHERE organize = %s """ % (organize)
    cur.execute(sql1)
    results1 = cur.fetchall()
    cur.execute(sql2)
    results2 = cur.fetchall()
    # 提交
    for row in results1:
        date = {"ID": str(row[0]), "SName": row[1], "Grade": row[2],
                "Telephone": str(row[4])}
        zzz.append(date)

    data = {'data': zzz, 'total': results2[0][0]}

    data = json.dumps(data, ensure_ascii=False)
    cur.close()
    conn.close()
    return data

@app.route('/select/id', methods=['POST', 'GET'])#按ID查询
def select_id():
    conn = get_connection()
    cur = conn.cursor()
    a = request.get_data()
    a = str(a, 'utf-8')
    a = json.loads(a)
    print(a)
    ID = a["ID"]
    zzz=[]
    sql1 = """SELECT * FROM student WHERE ID = %s """  % (ID)
    sql2 = """SELECT count(*) FROM student WHERE ID = %s """ % (ID)
    cur.execute(sql1)
    results1 = cur.fetchall()
    cur.execute(sql2)
    results2 = cur.fetchall()
    # 提交
    for row in results1:
        date = {"ID": str(row[0]), "SName": row[1], "Grade": row[2],
                "Organize": str(row[3]),"Telephone": str(row[4]),"QQ": str(row[5]),"WeChat": str(row[6]),
                "Mailbox": str(row[7]),"Other": str(row[8]),"EntryName": str(row[9]) ,
                "Winning": str(row[10]),"Code": str(row[11]),"Occupation": str(row[12]),
                "WorkAddress": str(row[13]) ,
                "Direction": str(row[14])}
        zzz.append(date)
    data = {'data': zzz, 'total': results2[0][0]}
    data = json.dumps(data, ensure_ascii=False)
    cur.close()
    conn.close()
    return data

@app.route('/select/name', methods=['POST', 'GET'])#按姓名查询
def select_name():
    conn = get_connection()
    cur = conn.cursor()
    a = request.get_data()
    a = str(a, 'utf-8')
    a = json.loads(a)
    print(a)
    SName = a["SName"]
    zzz=[]
    sql1 = """SELECT * FROM student WHERE SName = %s """  % (SName)
    sql2 = """SELECT count(*) FROM student WHERE SName = %s """ % (SName)
    cur.execute(sql1)
    results1 = cur.fetchall()
    cur.execute(sql2)
    results2 = cur.fetchall()
    # 提交
    for row in results1:
        date = {"ID": str(row[0]), "SName": row[1], "Grade": row[2],
                "Organize": str(row[3]),"Telephone": str(row[4]),"QQ": str(row[5]),"WeChat": str(row[6]),
                "Mailbox": str(row[7]),"Other": str(row[8]),"EntryName": str(row[9]) ,
                "Winning": str(row[10]),"Code": str(row[11]),"Occupation": str(row[12]),
                "WorkAddress": str(row[13]) ,
                "Direction": str(row[14])}
        zzz.append(date)
    data = {'data': zzz, 'total': results2[0][0]}
    data = json.dumps(data, ensure_ascii=False)
    cur.close()
    conn.close()
    return data




@app.route('/add/input', methods=['POST', 'GET'])#录入信息
def add_input():
    conn = get_connection()
    cur = conn.cursor()
    if request.method == 'GET':
        return render_template('login.html')

    SName = request.form.get('SName')  # 项目id
    Grade = request.form.get('Grade')  # 项目id
    Organize = request.form.get('Organize')  # 项目id
    Telephone = request.form.get('Telephone')  # 项目id
    QQ = request.form.get('QQ')  # 项目id
    WeChat = request.form.get('WeChat')  # 项目id
    Mailbox = request.form.get('Mailbox')  # 项目id
    Other = request.form.get('Other')  # 项目id
    EntryName = request.form.get('EntryName')  # 项目id
    Winning = request.form.get('Winning')  # 项目id
    Code = request.form.get('Code')  # 项目id
    Occupation = request.form.get('Occupation')  # 项目id
    WorkAddress = request.form.get('WorkAddress')  # 项目id
    Direction = request.form.get('Direction')  # 项目id

    if(SName == '' or Grade == ''  or Organize == '' ):
        return render_template('error1.html')

    sql1 = """insert into student (SName,Grade,Organize,Telephone,QQ,WeChat,Mailbox,Other,EntryName,Winning,Code,Occupation,WorkAddress,Direction) 
    values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') """ \
    % (SName,Grade,Organize,Telephone,QQ,WeChat,Mailbox,Other,EntryName,Winning,Code,Occupation,WorkAddress,Direction)

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
        return render_template('error2.html')
    finally:
        cur.close()
        conn.close()

    return render_template('login1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
