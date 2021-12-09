import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "asdf"   #암호키 발행

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/')
def index():
    if 'userID' in session:     #session에 userID가 존재하면
        ssid = session.get('userID')    #session을 가져옴
        return render_template('index.html', ssid = ssid)
    else:
        return render_template('index.html')   #index로 보내기

@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall()     #db에서 검색한 데이터
    conn.close()
    if 'userID' in session:  # session에 userID가 존재하면
        ssid = session.get('userID')  # session을 가져옴
        return render_template('memberlist.html', ssid=ssid, rs = rs)
    else:
        return render_template('memberlist.html')

@app.route('/member_view/<string:id>')
def member_view(id):    #mid를 경로로 설정하고 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' " % (id)   #문자열(%s로 사용) % 변수
    cur.execute(sql)
    rs = cur.fetchone() #해당 1개의 자료 반환받음
    conn.close()
    if 'userID' in session:  # session에 userID가 존재하면
        ssid = session.get('userID')  # session을 가져옴
        return render_template('member_view.html', rs=rs, ssid=ssid)
    else:
        return render_template('member_view.html')

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 자료 수집
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        date = request.form['regDate']

        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member VALUES ('%s', '%s', '%s', '%s', '%s')"\
                % (id, pwd, name, age, date)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('memberlist'))  #url 경로로 이동

    else:
        return render_template('register.html') #GET방식

@app.route("/login/", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        # 자료 전달받음
        id = request.form['mid']
        pwd = request.form['passwd']

        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s' " % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone() #db에서 일치하는 데이터 가져옴
        conn.close()
        if rs:
            session['userID'] = id
            return redirect(url_for('index'))
        else:
            error = "아이디나 비밀번호가 일치하지 않습니다."
            return render_template('login.html', error=error)

    else:
        return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('userID')   #세션 삭제
    return redirect(url_for('index'))

@app.route('/member_del/<string:id>/')
def member_del(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('memberlist'))

@app.route('/member_edit/<string:id>/', methods = ['GET', 'POST'])
def member_edit(id):
    if request.method == 'POST':
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        date = request.form['regDate']

        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE member SET passwd = '%s' , name = '%s', age = '%s', regDate = '%s' " \
              "WHERE mid = '%s' " % (pwd, name, age, date, id)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('member_view', id=id))

    else:
        #회원 자료 가져오기
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' " % (id)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        if 'userID' in session:
            ssid = session.get('userID')
            return render_template('member_edit.html', rs=rs, ssid=ssid)
        else:
            return render_template('member_edit.html')


app.run(debug=True)