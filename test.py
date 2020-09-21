class Db:
    host = '132.232.63.133'
    admin_user = 'root'
    def sql(self, sql_req='select * from accout'):
        # 连接database
        conn = pymysql.connect(Db.host, 'root', 'rootroot', 'accbook')
        cursor = conn.cursor()
        cursor.execute(sql_req)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res
