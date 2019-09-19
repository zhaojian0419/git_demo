"""
============================
Author:赵健
Date:2019-09-01
Time:16:28
E-mail:948883947@qq.com
File:constants.py
============================

"""
import os
# 项目路径
OB_DIR = os.path.dirname(os.path.dirname(__file__))
# 测试用例表格存储路径
DATA_DIR = os.path.join(OB_DIR, 'data')
# 配置文件存储路径
CF_DIR = os.path.join(OB_DIR, 'configs')
# 日志存储路径
LOGS_DIR = os.path.join(OB_DIR, 'logs')
# 测试报告存储路径
REPORT_DIR = os.path.join(OB_DIR, 'report')
# 测试用例类存储路径
CASES_DIR = os.path.join(OB_DIR, 'testcases')