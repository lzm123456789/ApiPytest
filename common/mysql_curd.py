import pymysql
from log.log import Log as mylog


class Mysql:
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
            mylog.error(f"连接mysql服务器失败, 具体原因: {e}")
            return None

    def search(self, sql, is_single_value=1, is_dict=0):
        """
        sql查询
        :param sql:
        :param is_single_value: 查询的结果是否为单个值, 默认是
        :param is_dict: 查询的结果是否为字典类型, 默认不是
        :return: 单个值或者列表
        """

        value = ''
        rows = []
        conn = self.connect()
        try:
            if conn:
                cur = conn.cursor() if not is_dict else conn.cursor(cursor=pymysql.cursors.DictCursor)
                cur.execute(sql)
                rows = cur.fetchall()
        except Exception as e:
            mylog.error(f"查询失败，具体原因: {e}")
        finally:
            conn.close()
        # 当sql不是查询单个值的时候
        if not is_single_value:
            return rows
        # 当sql是查询单个值的时候
        else:
            # 当查询不为空的时候
            if rows:
                value = rows[0][0]
            # 当查询为空的时候
            else:
                mylog.error("查询为空！")
            return value

    def update(self, sql, is_self_exist_semicolon=0):
        """
        sql增删改
        :param sql: 被执行的sql语句需以分号结尾, 多条就以分号分割
        :param is_self_exist_semicolon: sql语句自身是否包含分号, 默认不含
        :return: True或者False
        """

        sign = False
        conn = self.connect()
        try:
            if conn:
                cur = conn.cursor()
                # 当sql自身不包含分号的时候
                if is_self_exist_semicolon == 0:
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
            mylog.error(f"执行失败，具体原因: {e}")
            conn.rollback()
        finally:
            conn.close()
        return sign

    def procedure(self, procedure_name, parameters_list):
        """
        执行存储过程
        :param procedure_name: 存储过程名
        :param parameters_list: 参数列表
        :return: True或者False
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
            mylog.error(f"存储过程执行失败，具体原因: {e}")
        finally:
            cur.close()
            conn.close()
        return sign
