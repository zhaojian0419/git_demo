"""
============================
Author:赵健
Date:2019-08-30
Time:20:53
E-mail:948883947@qq.com
File:test_01_register_login.py
============================

"""
import unittest
import os
from package_lib.ddt import ddt, data
from common.openpyxl_object import ReadExcelData
from common.http_request import HttpRequest
from common.mylog import MyLog
import common.constants as cons  # 导入常量模块
from common.ob_mysql import ObMysql
from common.params_case import Replace  # 导入替换用例参数模块
from common.random_mobile import update_phone # 导入更新手机号方法
from common.ob_config import ob



@ddt
class TestCaseRegisterLogin(unittest.TestCase):
    '''注册测试用例'''
    test_case = os.path.join(cons.DATA_DIR, 'testcase.xlsx')  # 测试用例存放的路径
    excel = ReadExcelData(test_case, 'register-login')  # 读取表格的对象
    case_list = excel.read()  # 获取表格对象列表
    mylog = MyLog('mylog')

    @classmethod
    def setUpClass(cls):
        print('{}测试开始执行'.format(cls))
        cls.ms = ObMysql()  # 创建数据库操作对象,打开数据库
        cls.mylog.info('-----注册登录模块开始测试-----')

    def setUp(self):
        print('{}测试用例开始执行'.format(self))


    @data(*case_list)  # 对表格对象进行拆包
    def test(self, items):
        case_id = items.case_id        # 获取case_id
        title = items.title            # 获取title
        method = items.method          # 获取请求方法
        url = ob.getstr('url', 'url') + items.url   # 获取url地址
        rp = Replace(section1='register', section2='login')  # 创建替换对象
        data = eval(rp.replace_data(items.data))  # 替换后的数据
        except_result = items.except_result  # 获取预期结果
        print('第{}条用例开始执行：{}'.format(case_id, title))
        self.mylog.info('第{}条用例开始执行：{}'.format(case_id, title))  # 打印日志
        res = HttpRequest(url=url, data=data).httprequest(method=method).content.decode('utf8')  # 请求获取实际结果
        print('实际结果为{}'.format(except_result))
        print('预期结果为{}'.format(res))
        # 比对实际与预期结果
        try:
            self.assertEqual(res, except_result)
            if items.check_sql:  # 如果需要数据库校验
                sql = rp.replace_data(items.check_sql)
                sql_result = self.ms.find_result(sql)  # 数据库查询结果
                if sql_result == 1:  # 如果注册成功
                    ob.write('login', 'phone', data['mobilephone'])  # 将手机号写进配置文件
                    ob.write('login', 'pwd', data['pwd'])   # 将密码写进配置文件
                self.assertEqual(1, sql_result)  # 比对查询结果
        except AssertionError as e:   # 若实际与预期不符
            print('测试未通过')
            self.excel.write(row=case_id + 1, column=9, value='未通过')  # 回写测试结果
            self.mylog.error('测试未通过,未通过信息为：{}'.format(e))
            raise e   # 抛出异常
        else:
            print('测试通过')
            self.excel.write(row=case_id + 1, column=9, value='通过')  # 回写测试结果
            self.mylog.info('测试通过')  # 打印日志
        finally:
            self.excel.write(row=case_id + 1, column=8, value=res)  # 回写实际结果

    def tearDown(self):
        print('{}测试用例执行完毕'.format(self))
        update_phone()  # 更新手机号码和登录密码

    @classmethod
    def tearDownClass(cls):
        print('{}测试执行结束'.format(cls))
        cls.ms.close()  # 关闭数据库
        cls.mylog.info('-----注册登录模块测试执行结束-----')