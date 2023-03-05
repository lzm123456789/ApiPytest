# coding=utf-8
import pymysql
from log.log import MyLog as log


class MysqlCURD:
    def __init__(self, host, user, password, database, port=3306, charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset

    def connect(self):
        try:
            return pymysql.connect(host=self.host,
                                   port=self.port,
                                   user=self.user,
                                   password=self.password,
                                   database=self.database,
                                   charset=self.charset)
        except Exception as e:
            log.error(f"连接数据库失败，具体原因: {e}")
            return None

    def mysql_r(self, sql, column=None, is_dict=0):
        """
        执行查询sql
        :param sql:
        :param column: 是否查询单个字段
        :param is_dict: 返回结果是否为字典类型
        :return:
        """

        rows = value = []
        conn = self.connect()
        try:
            if conn:
                cur = conn.cursor()
                if is_dict:
                    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
                cur.execute(sql)
                rows = cur.fetchall()
        except Exception as e:
            log.error(f"查询失败，具体原因: {e}")
        finally:
            conn.close()
        if is_dict:
            return rows[0]
        # 当sql没有指定具体查询字段的时候
        if not column:
            return rows
        # 当sql指定了具体查询字段的时候
        else:
            # 当查询不为空的时候
            if rows:
                value = rows[0][0]
            # 当查询为空的时候
            else:
                log.error("查询为空！")
            return value

    def mysql_cud(self, sql, have_semicolon=0):
        """
        执行增删改sql
        :param sql: 被执行的sql语句需以分号结尾
        :param have_semicolon: sql语句自身是否包含分号
        :return:
        """

        sign = False
        conn = self.connect()
        try:
            if conn:
                cur = conn.cursor()
                # 当sql自身不包含分号的时候
                if have_semicolon == 0:
                    # 把多条sql语句分割开，然后逐条执行
                    sqllist = sql.split(';')[:-1]
                    for i in sqllist:
                        cur.execute(i)
                        conn.commit()
                # 当sql自身包含分号的时候
                else:
                    cur.execute(sql)
                    conn.commit()
                sign = True
        except Exception as e:
            log.error(f"执行失败，具体原因: {e}")
            conn.rollback()
        finally:
            conn.close()
        return sign

    def mysql_ep(self, procedure_name, parameters_list):
        """
        执行存储过程
        :param procedure_name: 存储过程名
        :param parameters_list: 参数列表
        :return:
        """

        sign = False
        conn = self.connect()
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            if conn:
                cur.callproc(procedure_name, args=parameters_list)
                conn.commit()
                sign = True
        except Exception as e:
            log.error(f"存储过程执行失败，具体原因: {e}")
        finally:
            cur.close()
            conn.close()
        return sign
