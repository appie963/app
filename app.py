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


# print(sql_insert("123", "1231"))


class Db:
    def sql_init(self, sql_req='select * from accout',
                 host='132.232.63.133',
                 admin_user='root',
                 admin_password='rootroot',
                 db_name='accbook'):
        conn = pymysql.connect(host, admin_user, admin_password, db_name)
        cursor = conn.cursor()
        cursor.execute(sql_req)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res


db_con = Db()
db_con.sql_init()


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
        print(user_name)
        print(user_passwd)
    if user_name == user_info and user_passwd == user_info:
        return True
    else:
        return False

# print(login_acc("123","1231"))




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
