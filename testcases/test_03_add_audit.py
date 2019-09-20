"""
============================
Author:赵健
Date:2019-09-08
Time:17:54
E-mail:948883947@qq.com
File:test_03_add_audit.py
============================

"""
import unittest
from package_lib.ddt import ddt, data
from common.mylog import MyLog
from common.openpyxl_object import ReadExcelData
import common.constants as con
from common.ob_mysql import ObMysql
import os
from common.params_case import Replace, ConText
from common.ob_config import ob
from common.http_session import HttpSession
from common.precondition_context import PreClass  # 导入前置条件类



@ddt
class TestCaseAddAudit(unittest.TestCase):
    '''添加项目审核测试用例'''
    mylog = MyLog('mylog')
    test_case = os.path.join(con.DATA_DIR, 'testcase.xlsx')  # 测试用例存放的路径
    excle = ReadExcelData(test_case, 'add-audit')  # 创建读取excle表格的对象
    case_list = excle.read()  # 读取测试用例的数据

    @classmethod
    def setUpClass(cls):
        print('{}测试开始执行'.format(cls))
        cls.mysql = ObMysql()  # 创建数据库连接
        pr = PreClass()
        pr.recharge()  # 预置前置条件，注册、登录、充值
        cls.mylog.info('-----添加项目、审核模块测试开始执行-----')

    def setUp(self):
        print('{}测试用例开始执行'.format(self))

    @data(*case_list)
    def test(self, items):
        rp = Replace()  # 创建替换对象

        # 获取测试用例的数据
        case_id = items.case_id  # 用例数据的编号
        title = items.title  # 用例的标题

        method = items.method  # 请求方法
        url = ob.getstr('url', 'url') + items.url  # 请求地址
        except_result = str(items.except_result)  # 获得预期结果
        data = items.data
        if items.interface == 'add':
            if items.check_sql:
                result1 = self.mysql.find_result(rp.replace_data(items.check_sql))  # 查询加标之前的个数
        if "@memberId@" in items.data:
            max_memberid = self.mysql.select(sql="SELECT max(Id)From member ", row=1)[0]  # 查到用户表的最大id

            data = data.replace("@memberId@", str(max_memberid + 100))
        data = eval(rp.replace_data(data))  # 替换后的申请数据

        print('第{}条用例开始执行：{}'.format(case_id, title))  # 打印信息
        self.mylog.info('第{}条用例开始执行：{}'.format(case_id, title))  # 写进日志
        # 发送请求获取实际结果
        res = HttpSession(url=url, data=data).httprequest(method=method).json()['code']
        # 比对实际与预期结果
        print('预期结果：{}'.format(except_result))
        print('实际结果:{}'.format(res))
        try:
            self.assertEqual(except_result, res)
            if items.check_sql:  # 如果需要数据库校验
                if items.interface == 'add':  # 如果接口为添加项目
                    select_result = self.mysql.find_result(rp.replace_data(items.check_sql))  # 得到查询结果
                    self.assertEqual(1, select_result-result1)  # 比对查询的结果与预期的结果
                    loanId = self.mysql.select(rp.replace_data(items.check_sql))[0][0]  # 获取到项目id
                    setattr(ConText, "loanId", loanId)  # 将项目id 写进临时类当中
                if items.interface == 'audit':
                    status = self.mysql.select(rp.replace_data(items.check_sql))[0][0]
                    self.assertEqual(eval(items.data)["status"], status)
        except AssertionError as e:
            print('{}测试用例未通过'.format(title))
            self.mylog.error('{}测试用例未通过,未通过的信息为{}'.format(title, e))  # 打印日志信息
            self.excle.write(row=case_id + 1, column=9, value='未通过')  # 回写测试结果
            raise e  # 抛出异常
        else:
            print('{}测试用例通过'.format(title))
            self.mylog.error('{}测试用例通过'.format(title))  # 打印日志信息
            self.excle.write(row=case_id + 1, column=9, value='通过')  # 回写测试结果
        finally:
            self.excle.write(row=case_id + 1, column=8, value=res)  # 回写实际结果

    def tearDown(self):
        print('{}测试执行完毕'.format(self))

    @classmethod
    def tearDownClass(cls):
        print('{}测试执行结束'.format(cls))
        cls.mylog.info('-----添加项目、审核模块测试执行结束-----')
        cls.mysql.close()  # 关闭数据库
