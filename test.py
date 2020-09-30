import pymysql

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
    # print(res)


d = Db(db_info)
