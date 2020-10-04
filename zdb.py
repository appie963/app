import pymysql


class zdb:

    def __init__(self, o):
        """
        初始化时,传入数据库配置
        :param o: 数据库参数,应包括主机名(ip地址) user(数据库账号) pwd(数据库密码) db(数据库)
        """
        if 'host' in o and 'user' in o and 'pwd' in o and 'db' in o:
            self.o = o
        self._conn = pymysql.connect(self.o['host'], self.o['user'], self.o['pwd'], self.o['db'])
        self._cur = self._conn.cursor()
        # 判断_cur与_conn钩子函数是否成功
        if self._conn and self._cur:
            pass
        else:
            raise ConnectionError  # 异常抛出

    def __table_name(self, table_index):
        """
        （私有）返回数据库表名
        :param table_index:输入参数为0或1
        :return: 返回字符串‘accout’或‘userlist’，若发生错误返回NameError
        """
        if table_index == 0 or table_index == 'accout':
            return self.o['table_name'][0]
        elif table_index == 1 or table_index == 'userlist':
            return self.o['table_name'][1]
        else:
            raise NameError

    def __commit_db(self, sql_cmd):
        try:
            self._cur.execute(sql_cmd)
            self._conn.commit()
        except ConnectionError:
            # 如果发生错误则回滚
            self._conn.rollback()

    def __close(self):
        """
        断开连接方法
        :return: None
        """
        self._cur.close()
        self._conn.close()
        return self

    def query(self, tb_name, line, row='*', ):
        # query db_info['table_name']
        # need: sql_cmd,table_name
        # return list of table
        """
        查询
        :param tb_name:使用（私有）查询表名方法输入0或1
        :param line: 输入查询行数 1，n，all或*
        :param row:后接 select * from xxx 或 select row from xxx
        :return:返回查询的内容
        """
        sql_cmd = 'select ' + row + ' from ' + self.__table_name(tb_name)
        self._cur.execute(sql_cmd)
        if line == 1:
            return self._cur.fetchone()
        elif line != 1 and type(line) == int:
            return self._cur.fetchmany(line)
        if line == 'all' or '' or '*':
            return self._cur.fetchall()
        self.__close()

    def insert(self, table_name, field, *value):
        value = str(value)[1:-1]
        print(value)
        # 正确传入参数格式如下：
        # db.insert(1, 'username,password', 'test_name', 'pwd')
        sql_cmd = "insert into %s (%s) values (%s) " % (self.__table_name(table_name), field, value)
        # 执行sql语句
        print(value)
        print(sql_cmd)
        self.__commit_db(sql_cmd)
        self.__close()
        return self
