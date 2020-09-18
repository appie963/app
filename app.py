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


all_usertable = sql('select * from usertable')
for oneList in all_usertable:
    print()

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


# 登录认证界面
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
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
