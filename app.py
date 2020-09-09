from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)


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
    login_name = 'admin'
    login_passwd = 'admin123'
    if request.method == 'POST' and request.form['nm'] == login_name and request.form['passwd'] == login_passwd:
        user = request.form['nm']
        return render_template('success.html', user=user)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=80)
