# 初始化
from flask import Flask, redirect, url_for, request, render_template
from zdb import zdb
from config import *

app = Flask(__name__)

# 加载自定义库zdb
db = zdb(db_info)


def login_acc(user_name, user_passwd):
    """
    判断用户名密码
    :param user_name:用户名
    :param user_passwd:密码
    :return:返回true或false
    """
    all_usertable = db.query('userlist', '*')

    for user_info in all_usertable:
        if user_name in user_info and user_passwd in user_info:
            return True
    return False


# login_acc('test1', 'pwd')


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


@app.route('/login', methods=['POST'])
def login():
    # 登陆认证
    print(login_acc(request.form['nm'], request.form['passwd']))
    if request.method == 'POST' and login_acc(request.form['nm'], request.form['passwd']):
        return render_template('blog.html', user=request.form['nm'], passwd=request.form['passwd'])
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
