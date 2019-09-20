"""
============================
Author:赵健
Date:2019-08-27
Time:23:03
E-mail:948883947@qq.com
File:run_test.py
============================

"""
import unittest
import time
import os
import common.constants as cons  # 导入常量模块  # 导入操作配置文件ob对象
from HTMLTestRunnerNew import HTMLTestRunner  # 从HTMLTestRunnerNew模块导入HTMLTestRunner类


test_case = cons.CASES_DIR # 得到存储测试用例模块的路径
save_report = cons.REPORT_DIR  # 测试报告存储目录
now = time.strftime('%Y-%m-%d')  # 得到当前时间
path = os.path.join(save_report, 'report_{}.html'.format(now))  # 测试报告文件位置
suite = unittest.TestSuite()  # 创建测试套件
loader = unittest.TestLoader()  # 创建加载对象
suite.addTest(loader.discover(test_case))
with open(path, 'wb') as fb:  # 将测试结果写入测试报告
    runner = HTMLTestRunner(stream=fb,
                            verbosity=2,
                            title='TestReport',
                            description='测试报告',
                            tester='zj')
    runner.run(suite)  # 执行测试用例
