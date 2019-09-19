"""
============================
Author:赵健
Date:2019-09-05
Time:22:49
E-mail:948883947@qq.com
File:random_mobile.py
============================

"""

import random
import string
import re
from common.ob_mysql import ObMysql  # 导入操作数据库模块
from common.ob_config import ob  # 导入操作配置文件对象

mysql = ObMysql()


def random_phone():
    '''随机生成11位手机号码'''
    while True:
        phone = '13'  # 定义手机号码开头
        for i in range(9):  # 随机生成9个数字
            c = random.randint(0, 9)
            phone += str(c)
        if not mysql.find_result('SELECT * FROM member WHERE MobilePhone = {}'.format(phone)):  # 如果数据库没有该手机号
            return phone  # 返回手机号码


def random_pwd():
    '''随机生成8位密码'''
    while True:
        src = string.ascii_letters + string.digits  # 生成包含大写、小写、数字的密码
        pwd_list = random.sample(src, 8)  # 随机8位密码列表
        pwd = ''.join(pwd_list)  # 随机8位密码
        if (re.search('[A-Z]', pwd) and
                re.search('[a-z]', pwd) and
                re.search(r'\d', pwd)):
            return pwd    # 如果8位密码包含数字，大小写字母，返回密码


def update_phone():
    '''更新配置文件手机号'''
    phone = random_phone()  # 获取手机号
    ob.write('register', 'phone', phone)  # 写进配置文件
    pwd = random_pwd()  # 获取密码
    ob.write('register', 'pwd', pwd)  # 写进配置文件


if __name__ == '__main__':

   update_phone()
