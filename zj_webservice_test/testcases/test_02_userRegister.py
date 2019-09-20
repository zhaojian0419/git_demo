"""
============================
Author:赵健
Date:2019-09-16
Time:22:25
E-mail:948883947@qq.com
File:test_02_userRegister.py
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




@ddt
class TestUserRegister(unittest.TestCase):
    '''注册'''
    mylog = MyLog('mylog')  # 创建日志对象
    test_case = os.path.join(con.DATA_DIR, 'testcase.xlsx')  # 获取测试用例存放路径
    excle = ReadExcelData(test_case, 'userRegister')
    test_list = excle.read()  # 获取数据列表对象
    pr = PreClass()  # 创建前置条件对象


    @classmethod
    def setUpClass(cls):


        cls.mysql = ObMysql(database='user_db')  # 建立数据库连接对象
        cls.mylog.info('-----注册测试开始执行-----')
        print('{}开始测试'.format(cls))

    def setUp(self):
        print('{}开始测试'.format(self))

    @data(*test_list)
    def test(self, items):
        self.pr.sendMCode()   # 发送短信验证码
        rp = Replace()  # 创建替换对象
        case_id = items.case_id  # 获取用例编号
        url = ob.getstr('url', 'url') + items.url
        data = items.data   # 获取数据
        title = items.title  # 获取用例标题
        if "@verify_code@" in data:
            verify_code = int(getattr(ConText, 'verify_code')) + 1
            data = data.replace("@verify_code@", str(verify_code))  # 用最新的验证码去替换
        if title == '验证码超时':
            verify_code = ob.getstr("verify_phone", "verify_code")  # 拿到已经超时的验证码
            phone = ob.getstr("verify_phone", "phone")  # 拿到发送的手机号
            data = data.replace("<verify_code>", verify_code)  # 替换验证码
            data = data.replace("<phone>", phone)  # 替换手机号码
        client = Client(url)  # 创建连接
        data = eval(rp.replace_data(data))  # 获取请求数据
        print("请求数据为：", data)
        except_result = str(items.except_result)  # 获取预期结果,并转换为字典
        print('第{}条测试用例：{}开始执行'.format(case_id, title))
        re = client.service.userRegister(data)  # 发送请求
        acl_re = str(re.retCode)  # 获取实际结果
        print('实际结果:{}'.format(except_result), type(except_result))
        print('预期结果:{}'.format(acl_re), type(acl_re))
        print(dict(re))
        # 比对实际结果与预期结果
        try:
            self.assertEqual(except_result, acl_re)
            if items.check_sql:
                sql = rp.replace_data(items.check_sql)
                slect_result = self.mysql.find_result(sql)  # 得到查询结果
                self.assertEqual(1, slect_result)
                re_username = data["user_id"]  # 拿到注册过的用户名
                re_phone = data["mobile"]
                setattr(ConText, 're_username', re_username)  # 将注册过后的用户名写进临时变量
                setattr(ConText, 're_phone', re_phone)  # 将注册过后的手机号码写进临时变量
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
        update_phone()  # 更新手机号码和登录密码


    @classmethod
    def tearDownClass(cls):
        print('{}测试执行结束'.format(cls))
        cls.mysql.close()  # 关闭数据库
        cls.mylog.info('-----注册模块测试执行结束-----')