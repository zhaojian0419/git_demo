"""
============================
Author:赵健
Date:2019-09-04
Time:20:59
E-mail:948883947@qq.com
File:ob_mysql.py
============================

"""
import pymysql
from common.ob_config import ob


class ObMysql(object):
    def __init__(self):
        # 建立数据库的链接
        try:
            self.conn = pymysql.connect(
                host=ob.getstr('mysql', 'host'),
                user=ob.getstr('mysql', 'user'),
                passwd=ob.getstr('mysql', 'passwd'),
                port=ob.getint('mysql', 'port'),
                database=ob.getstr('mysql', 'database'),
                charset='utf8'
            )
        except Exception as e:  # 报错给出提示
            print('出错：{}'.format(e))
        else:
            # 获取操作游标
            self.cursor = self.conn.cursor()

    def select(self, sql, row=0):
        '''
        查询发法
        :param sql: sql语句
        :param row: 查询的行数（默认为0，全都查询）
        :return: 查询结果
        '''
        try:
            self.cursor.execute(sql)  # 执行sql语句
            self.conn.commit()        # 提交事务
        except Exception as e:   # 报错给出提示
            print('出错{}'.format(e))
        else:
            if row == 0:   # 如果行数为默认值，查询全部内容
                res = self.cursor.fetchall()
                return res
            elif row == 1:  # 如果行数为1，查询单行内容
                res = self.cursor.fetchone()
                return res
            elif row > 1:  # 如果行数大于1，查询多行内容
                res = self.cursor.fetchmany(row)
                return res
            else:    # 行数格式不对，给出提示
                print('输入行数格式错误，请核对')

    def find_result(self, sql):
        '''
        查询结果
        :param sql: sql语句
        :return: 返回查询结果
        '''
        try:
            res = self.cursor.execute(sql)   # 执行sql语句
            self.conn.commit()    # 提交事务
        except Exception as e:   # 报错给出提示
            print('出错{}'.format(e))
        else:
            return res   # 返回查询结果

    def other_ob(self, sql):
        '''
        其他操作方法
        :param sql: sql语句
        :return:
        '''
        try:
            self.cursor.execute(sql)  # 执行sql语句
            self.conn.commit()   # 提交事务
        except Exception as e:  # 报错给出提示
            print('出错：{}'.format(e))
            self.conn.rollback()  # 数据回滚

    def close(self):
        """关闭操作"""
        self.cursor.close()  # 关闭游标
        self.conn.close()   # 关闭连接

if __name__ == '__main__':
    sql = "SELECT id FROM member WHERE MobilePhone= '13351514645'"
    ms = ObMysql()
    res = ms.select(sql)

    row = ms.find_result(sql)
    r = res[0][0]
    print(r,type(r))
    ms.close()



