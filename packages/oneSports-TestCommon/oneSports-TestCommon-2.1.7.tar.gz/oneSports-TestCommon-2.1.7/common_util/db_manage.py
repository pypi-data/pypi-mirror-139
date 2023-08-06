import psycopg2


class DBConnect(object):
    def __init__(self, dbConfig):
        self.db_conf = dbConfig
        # 获取连接对象
        self.conn = psycopg2.connect(
            host=self.db_conf.host,
            port=self.db_conf.port,
            user=self.db_conf.user,
            password=self.db_conf.password,
            database=self.db_conf.database
        )
        # 获取数据的游标
        self.cur = self.conn.cursor()

    def close_connect(self):
        # 关闭数据连接
        # 游标关闭
        self.cur.close()
        # 连接对象关闭
        self.conn.close()

    def delete_user(self, username):
        """删除指定的对象数据"""
        sqlStr = "delete from sys_user where \"name\" like '{}%'".format(username)
        self.cur.execute(sqlStr)
        self.conn.commit()
