from flask import Flask, redirect, url_for, request, render_template
import pymysql

app = Flask(__name__)


def sql(sql_req='select * from accout'):
    # 连接database
    conn = pymysql.connect('132.232.63.133', 'root', 'rootroot', 'accbook')
    cursor = conn.cursor()
    cursor.execute(sql_req)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res


def sql_insert(username, password):
    conn = pymysql.connect('132.232.63.133', 'root', 'rootroot', 'accbook')
    cursor = conn.cursor()
    sql_cmd = "INSERT INTO userlist(username, password) VALUES ('%s', '%s')" % (username, password)

    try:
        # 执行sql语句
        cursor.execute(sql_cmd)
        # 执行sql语句
        conn.commit()
    except:
        # 发生错误时回滚
        conn.rollback()
    cursor.execute('select * from userlist')

    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res


print(sql_insert("123","1231"))


# 首页自动跳转至login.html
@app.route('/')
def index():
    return render_template("login.html")


# 登录成功的入口
@app.route('/success')
def success():
    # 仅为登录成功的入口
    if request.method == 'GET':
        return render_template("404.html")
        # 判断是否为post方式路由不是则认定为直接访问，返回404
    else:
        return redirect(url_for('index'))


def login_acc(user_name, user_passwd):
    all_usertable = sql('select * from userlist')
    for user_info in all_usertable:
        print(user_info)
    if user_name in user_info and user_passwd in user_info:
        return True
    else:
        return False


@app.route('/login', methods=['POST'])
def login():
    # 登陆认证
    if request.method == 'POST' and login_acc(request.form['nm'], request.form['passwd']):
        return render_template('success.html', user=request.form['nm'], passwd=request.form['passwd'])
    else:
        return redirect(url_for('index'))


@app.route('/_register')
def _register():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register():
    # 判断是否为post请求
    if request.method == 'POST':
        print(request.form['reg_name'])
        print(request.form['reg_passwd'])

        return render_template('success.html', user=request.form['reg_name'], passwd=request.form['reg_passwd'])
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=80)
