"""
============================
Author:赵健
Date:2019-08-24
Time:20:36
E-mail:948883947@qq.com
File:ob_config.py
============================

"""
import common.constants as cons  # 导入常量模块
import os
from configparser import ConfigParser


class ObConfig(object):
    '''操作配置文件'''
    cf_path = os.path.join(cons.CF_DIR, 'env.ini')  # 配置文件路径
    conf = ConfigParser()
    conf.read(cf_path, encoding='utf8')
    switch = conf.getint('env', 'switch')
    if switch == 1:  # 如果switch==1 切换到测试环境
        configfile = os.path.join(cons.CF_DIR, 'case.ini')
    conf.read(configfile, encoding='utf8')  # 打开文件

    def write(self, stname, otname, value):
        '''
        写方法
        :param stname: section名
        :param otname: obtion名
        :param value: 写入的内容
        :return:
        '''

        if self.conf.has_section(stname):  # 判断配置文件中是否已存在section
            self.conf.set(stname, otname, value)  # 将option和值写进section
            with open(self.configfile, 'w', encoding='utf8') as fp:  # 写入
                self.conf.write(fp)
        else:  # 若不存在
            self.conf.add_section(stname)  # 创建section
            self.conf.set(stname, otname, value)  # 将option和值写进section
            with open(self.configfile, 'w', encoding='utf8') as fp:  # 写入
                self.conf.write(fp)

    def getint(self, stname, otname):
        '''
        查方法(整型)
        :param stname:section名
        :param otname:obtion名
        :return:
        '''

        if self.conf.has_section(stname):  # 判断配置文件中是否已存在section
            if self.conf.has_option(stname, otname):  # 判断配置文件中是否已存在option
                return self.conf.getint(stname, otname)  # 返回获取到的option的值
            else:
                print('不存在对应的option:{}'.format(otname))  # 不存在option给出提示
        else:
            print('不存在对应的section:{}'.format(stname))  # 不存在section给出提示

    def getstr(self, stname, otname):
        '''
        查方法(字符串)
        :param stname:section名
        :param otname:obtion名
        :return:
        '''

        if self.conf.has_section(stname):  # 判断配置文件中是否已存在section
            if self.conf.has_option(stname, otname):  # 判断配置文件中是否已存在option
                return self.conf.get(stname, otname)  # 返回获取到的option的值
            else:
                print('不存在对应的option:{}'.format(otname))  # 不存在option给出提示
        else:
            print('不存在对应的section:{}'.format(stname))  # 不存在section给出提示

    def getfloat(self, stname, otname):
        '''
        查方法(浮点)
        :param stname:section名
        :param otname:obtion名
        :return:
        '''

        if self.conf.has_section(stname):  # 判断配置文件中是否已存在section
            if self.conf.has_option(stname, otname):  # 判断配置文件中是否已存在option
                return self.conf.getfloat(stname, otname)  # 返回获取到的option的值
            else:
                print('不存在对应的option:{}'.format(otname))  # 不存在option给出提示
        else:
            print('不存在对应的section:{}'.format(stname))  # 不存在section给出提示

    def getboolean(self, stname, otname):
        '''
        查方法(布尔值)
        :param stname:section名
        :param otname:obtion名
        :return:
        '''

        if self.conf.has_section(stname):  # 判断配置文件中是否已存在section
            if self.conf.has_option(stname, otname):  # 判断配置文件中是否已存在option
                return self.conf.getboolean(stname, otname)  # 返回获取到的option的值
            else:
                print('不存在对应的option:{}'.format(otname))  # 不存在option给出提示
        else:
            print('不存在对应的section:{}'.format(stname))  # 不存在section给出提示

    def getother(self, stname, otname):
        '''
        查方法(其他类型)
        :param stname:section名
        :param otname:obtion名
        :return:
        '''

        if self.conf.has_section(stname):  # 判断配置文件中是否已存在section
            if self.conf.has_option(stname, otname):  # 判断配置文件中是否已存在option
                return eval(self.conf.get(stname, otname))  # 返回获取到的option的值
            else:
                print('不存在对应的option:{}'.format(otname))  # 不存在option给出提示
        else:
            print('不存在对应的section:{}'.format(stname))  # 不存在section给出提示


ob = ObConfig()  # 创建配置文件操作对象
if __name__ == '__main__':
    host = ob.getstr('mysql', 'host')
    print(host)
