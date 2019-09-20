"""
============================
Author:赵健
Date:2019-09-15
Time:16:01
E-mail:948883947@qq.com
File:test_06_get.py
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
from decimal import Decimal
from common.precondition_context import PreClass  # 导入前置条件类


@ddt
class TestCaseGet(unittest.TestCase):
    '''获取相关记录测试用例'''
    mylog = MyLog('mylog')
    test_case = os.path.join(con.DATA_DIR, 'testcase.xlsx')  # 测试用例存放的路径
    excle = ReadExcelData(test_case, 'get')  # 创建读取excle表格的对象
    case_list = excle.read()  # 读取测试用例的数据

    @classmethod
    def setUpClass(cls):
        print('{}测试开始执行'.format(cls))
        cls.mysql = ObMysql()  # 创建数据库连接
        pr = PreClass()
        pr.add()  # 借款人加标
        pr.recharge()  # 投资人登录并充值
        cls.mylog.info('-----获取相关记录测试开始执行-----')

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


        if "@memberId@" in items.data:
            max_memberId = self.mysql.select(sql="SELECT max(Id)From member", row=1)[0]  # 查到member表的最大标id
            data = data.replace("@memberId@", str(max_memberId + 100))
        data = eval(rp.replace_data(data))  # 替换后的申请数据
        print(data)

        print('第{}条用例开始执行：{}'.format(case_id, title))  # 打印信息
        self.mylog.info('第{}条用例开始执行：{}'.format(case_id, title))  # 写进日志
        # 发送请求获取实际结果
        res = HttpSession(url=url, data=data).httprequest(method=method).json()['code']
        # 比对实际与预期结果
        print('预期结果：{}'.format(except_result))
        print('实际结果:{}'.format(res))
        try:
            self.assertEqual(except_result, res)
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
        cls.mylog.info('-----获取相关记录测试执行结束-----')
        cls.mysql.close()  # 关闭数据库