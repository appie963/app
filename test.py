import pymysql


class Db:

    def __init__(self, host, admin_user, admin_password, db_name, table_name, sql_cmd):
        self.host = host
        self.admin_user = admin_user
        self.admin_password = admin_password
        self.db_name = db_name
        self.table_name = table_name
        self._conn = pymysql.connect(self.host, self.admin_user, self.admin_password, self.db_name)
        self._cur = self._conn.cursor()

        if self._conn and self._cur:
            pass
        else:
            print(NameError, '连接失败')
            exit(1)
        self.sql_cmd = sql_cmd

    def close(self):
        self._cur.close()
        self._conn.close()

    def query_all(self):
        self._cur.execute(self.sql_cmd)
        res = self._cur.fetchall()
        self.close()
        return res


d = Db(host='132.232.63.133',
       admin_user='root',
       admin_password='rootroot',
       db_name='accbook',
       table_name='accout', sql_cmd='select * from userlist')

print(d.query_all())
