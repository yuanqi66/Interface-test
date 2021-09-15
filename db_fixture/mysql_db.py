# @Time: 2021/8/30 16:09
# @File: mysql_db.py
# @Author: YuanQi
# @Email: 1252429141@qq.com

from pymysql import connect, cursors
from pymysql.err import OperationalError
import os
import configparser as cparser

# 读取db_config.ini文件设置
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")


# 创建DB类，封装MySQL基本操作
class DB:

    # __init__()方法初始化数据库连接
    def __init__(self):
        try:
            # 通过connect()方法连接数据库
            self.conn = connect(host=host,
                                user=user,
                                password=password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=cursors.DictCursor)
        except OperationalError as e:
            print("MySQL Error %d: %s" % (e.args[0], e.args[1]))

    # 清除数据表
    def clear(self, table_name):
        # real_sql = "truncate table" + table_name + ";"
        real_sql = "delete from " + table_name + ";"
        with self.conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)

        self.conn.commit()

    # 插入表数据
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
        # 使用join() 方法用于将序列中的key和value以指定的字符,分别连接生成一个字符串
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ");"
        print(real_sql)

        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)

        self.conn.commit()

    # 关闭数据库连接
    def close(self):
        self.conn.close()

    # 初始化数据
    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()


if __name__ == '__main__':
    db = DB()
    table_name = "sign_event"
    data = {'id': 1, 'name': '红米', '`limit`': 2000, 'status': 1, 'address': '北京会展中心',
            'start_time': '2021-08-20 00:25:42', 'create_time': '2021-08-20 00:25:42'}
    db.clear(table_name)
    db.insert(table_name, data)
    db.close()
