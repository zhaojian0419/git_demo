"""
============================
Author:赵健
Date:2019-09-17
Time:21:27
E-mail:948883947@qq.com
File:test_03_verifyUserAuth.py
============================

"""
import unittest
import suds
from suds.client import Client
from common.mylog import MyLog
from common.ob_mysql import ObMysql
from package_lib.ddt import ddt, data
import common.constants as con
from common.openpyxl_object import ReadExcelData
import os
from common.params_case import Replace, ConText
from common.random_mobile import update_phone
from common.ob_config import ob
from common.precondition_context import PreClass
from common.random_name_idcard import update




@ddt
class TestVerifyUserAuth(unittest.TestCase):
    '''实名认证'''
    mylog = MyLog('mylog')  # 创建日志对象
    test_case = os.path.join(con.DATA_DIR, 'testcase.xlsx')  # 获取测试用例存放路径
    excle = ReadExcelData(test_case, 'verifyUserAuth')
    test_list = excle.read()  # 获取数据列表对象
    pr = PreClass()  # 创建前置条件对象


    @classmethod
    def setUpClass(cls):


        cls.mysql = ObMysql(database='user_db')  # 建立数据库连接对象
        cls.mylog.info('-----实名认证模块测试开始执行-----')
        print('{}开始测试'.format(cls))

    def setUp(self):
        print('{}开始测试'.format(self))

    @data(*test_list)
    def test(self, items):
        self.pr.userRegister()   # 注册
        rp = Replace(section1="userinfo")  # 创建替换对象
        case_id = items.case_id  # 获取用例编号
        url = ob.getstr('url', 'url') + items.url
        data = items.data   # 获取数据
        title = items.title  # 获取用例标题
        if "@uid@" in data:
            max_uid = self.mysql.select(rp.replace_data(items.check_sql))[0][0]
            print(max_uid)
            data = data.replace("@uid@", str(int(max_uid+1)))  # 用最新uid去替换
        client = Client(url)  # 创建连接
        data = eval(rp.replace_data(data))  # 获取请求数据
        print("请求数据为：", data)
        except_result = str(items.except_result)
        print('第{}条测试用例：{}开始执行'.format(case_id, title))
        re = client.service.verifyUserAuth(data)  # 发送请求
        acl_re = str(re.retCode)  # 获取实际结果
        print('实际结果:{}'.format(except_result), type(except_result))
        print('预期结果:{}'.format(acl_re), type(acl_re))
        print(dict(re))
        # 比对实际结果与预期结果
        try:
            self.assertEqual(except_result, acl_re)
            if items.check_sql:
                if items.title == "实名认证成功" :
                    sql = rp.replace_data(items.check_sql)
                    slect_result = self.mysql.find_result(sql)  # 得到查询结果
                    self.assertEqual(1, slect_result)

        except AssertionError as e:
            print('{}用例测试未通过'.format(title))
            self.mylog.error('{}用例测试未通过'.format(title))  # 打印日志信息
            self.excle.write(row=case_id + 1, column=8, value='未通过')  # 回写测试结果
            raise e  # 抛出异常
        else:
            print('{}用例测试通过'.format(title))
            self.mylog.info('{}用例测试通过'.format(title))  # 打印日志信息
            self.excle.write(row=case_id + 1, column=8, value='通过')  # 回写测试结果
        finally:
            self.excle.write(row=case_id + 1, column=7, value=acl_re)  # 回写实际结果

    def tearDown(self):
        print('{}测试用例执行完毕'.format(self))
        update()  # 更新配置文件里面的姓名和身份证号码


    @classmethod
    def tearDownClass(cls):
        print('{}测试执行结束'.format(cls))
        cls.mysql.close()  # 关闭数据库
        cls.mylog.info('-----实名认证模块测试执行结束-----')