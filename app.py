import sqlite3

from flask import Flask, render_template

app = Flask(__name__)

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall()     #db에서 검색한 데이터
    conn.close()
    return render_template('memberlist.html', rs = rs)

@app.route('/member_view/<string:id>')
def member_view(id):    #mid를 경로로 설정하고 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' " % (id)   #문자열(%s로 사용) % 변수
    cur.execute(sql)
    rs = cur.fetchone() #해당 1개의 자료 반환받음
    conn.close()
    return render_template('member_view.html', rs = rs)

app.run(debug=True)