from flask import Flask, redirect, url_for, request, render_template
import pymysql

app = Flask(__name__)

db_info = {
    'host': '132.232.63.133',
    'user': 'root',
    'pwd': 'rootroot',
    'db': 'accbook',
    'table_name': ['accout', 'userlist']
}


class Db:

    def __init__(self, o):
        if 'host' in o and \
                'user' in o and \
                'pwd' in o and \
                'db' in o:
            self.o = o
        self._conn = pymysql.connect(self.o['host'], self.o['user'], self.o['pwd'], self.o['db'])
        self._cur = self._conn.cursor()
        # 判断_cur与_conn钩子函数是否成功
        if self._conn and self._cur:
            pass
        else:
            raise ConnectionError  # 异常抛出

    def close(self):
        self._cur.close()
        self._conn.close()

    def query(self, tb_name, line, row='*', ):
        # query db_info['table_name']
        # need: sql_cmd,table_name
        # return list of table
        sql_cmd = 'select ' + row + ' from ' + tb_name
        self._cur.execute(sql_cmd)
        if line == 1:
            return self._cur.fetchone()
        elif line != 1 and type(line) == int:
            return self._cur.fetchmany(line)

        if line == 'all' or '' or '*':
            return self._cur.fetchall()

    def insert(self, table_name, field, value):
        sql_cmd = "insert into '%s' ('%s') values ('%s') " % (str(table_name), str(field), str(value))
            # 执行sql语句
        print(sql_cmd)
        try:
            self._cur.execute(sql_cmd)
            self._conn.commit()
        except ConnectionError:
            # 如果发生错误则回滚
            self._conn.rollback()


db = Db(db_info)
# db.insert(db_info[0],field='',value='')
print(
db.query(db_info['table_name'][1], '*')
)
db.insert(db_info['table_name'][1], 'username,password', 'test_name,pwd')


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
    all_usertable = db.query(db_info['table_name'][1], '*')

    for user_info in all_usertable:
        if user_name == user_info[1] and user_passwd == user_info[2]:
            return True


# print(type(login_acc("admin", "password")))


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
