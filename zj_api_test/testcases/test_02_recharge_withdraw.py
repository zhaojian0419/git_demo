"""
============================
Author:赵健
Date:2019-09-01
Time:22:14
E-mail:948883947@qq.com
File:test_02_recharge_withdraw.py
============================

"""
import unittest
import os
from decimal import Decimal
from package_lib.ddt import ddt, data
from common.openpyxl_object import ReadExcelData
import common.constants as cons  # 导入常量模块
from common.http_session import HttpSession
from common.mylog import MyLog
from common.ob_mysql import ObMysql  # 导入操作数据库
from common.ob_config import ob
from common.params_case import Replace


@ddt
class TestCaseRechargeWithdraw(unittest.TestCase):
    '''充值提现测试用例'''
    test_case = os.path.join(cons.DATA_DIR, 'testcase.xlsx')  # 测试用例存放的路径
    excel = ReadExcelData(test_case, 'recharge-withdraw')  # 读取表格的对象
    case_list = excel.read()  # 获取表格对象列表
    mylog1 = MyLog('mylog')

    @classmethod
    def setUpClass(cls):
        url = ob.getstr('url', 'url') + '/member/login'
        phone = ob.getstr('login', 'phone')
        pwd = ob.getstr('login', 'pwd')
        login_data = {
            "mobilephone": phone,
            "pwd": pwd
        }   # 登录数据
        print('{}测试开始执行'.format(cls))
        cls.login = HttpSession(url=url, data=login_data).httprequest(method='post')  # 登录
        cls.ms = ObMysql()  # 创建数据库操作对象，打开数据库
        cls.mylog1.info('-----充值提现模块开始测试-----')

    def setUp(self):
        print('{}测试用例开始执行'.format(self))

    @data(*case_list)  # 对表格对象进行拆包
    def test(self, items):
        case_id = items.case_id  # 获取case_id
        title = items.title  # 获取title
        method = items.method  # 获取请求方法
        url = ob.getstr('url', 'url') + items.url  # 获取url地址
        rp = Replace(section2='login')
        data = eval(rp.replace_data(items.data))  # 获取请求数据
        except_result = str(items.except_result)  # 获取预期结果
        print('第{}条用例开始执行：{}'.format(case_id, title))
        self.mylog1.info('第{}条用例开始执行：{}'.format(case_id, title))  # 打印日志
        if items.check_sql:  # 如果需要校验数据库
            sql = rp.replace_data(items.check_sql)  # 获取sql语句
            select_result = self.ms.select(sql)  # 充值或者取现前的查询结果
            leave_amount = select_result[0][0]  # 拿到充值或者取现前的账户余额
            print(leave_amount)
            res = HttpSession(url=url, data=data).httprequest(method=method).json()  # 请求
            select_result1 = self.ms.select(sql)  # 充值后的查询结果
            if items.interface == 'recharge':  # 如果为充值接口
                except_leave_amount = leave_amount + Decimal(str(data['amount']))  # 得到预期的充值之后的余额
            elif items.interface == 'withdraw':  # 如果为取现接口
                except_leave_amount = leave_amount - Decimal(str(data['amount']))  # 得到预期提现后的余额
            leave_amount1 = select_result1[0][0]  # 拿到充值或者提现后后的账户余额
            print('充值或者取现前的账户余额为{}'.format(leave_amount))
            print('预期的账户余额为{}'.format(except_leave_amount))
            print('充值或者取现后的账户余额为{}'.format(leave_amount1))
        else:
            res = HttpSession(url=url, data=data).httprequest(method=method).json()  # 请求
        res1 = res['code']  # 返回的状态码

        print('实际结果为{}'.format(except_result))
        print('预期结果为{}'.format(res1))
        # 比对实际与预期结果
        try:
            self.assertEqual(res1, except_result)
            if items.check_sql:  # 如果需要校验数据库
                self.assertEqual(except_leave_amount, leave_amount1)  # 比对预期的充值之后的余额与实际的账户余额
        except AssertionError as e:  # 若实际与预期不符
            print('测试未通过')
            self.excel.write(row=case_id + 1, column=9, value='未通过')  # 回写测试结果
            self.mylog1.error('测试未通过,未通过信息为：{}'.format(e))  # 打印日志
            raise e  # 抛出异常
        else:
            print('测试通过')

            self.excel.write(row=case_id + 1, column=9, value='通过')  # 回写测试结果
            self.mylog1.info('测试通过')  # 打印日志
        finally:
            self.excel.write(row=case_id + 1, column=8, value=res1)  # 回写实际结果

    def tearDown(self):
        print('{}测试用例执行完毕'.format(self))

    @classmethod
    def tearDownClass(cls):

        print('{}测试执行结束'.format(cls))
        cls.login.close()  # 关闭session
        cls.ms.close()  # 关闭数据库
        cls.mylog1.info('-----充值提现模块测试执行结束-----')
