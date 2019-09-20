"""
============================
Author:赵健
Date:2019-08-27
Time:22:24
E-mail:948883947@qq.com
File:mylog_new.py
============================

"""
import logging
import time
import os
from le_python自动化.zj_apt_test.common.ob_config import ob  # 从操作配置文件导入ob对象


class MyLog(object):
    '''日志类'''

    def __new__(cls, *args, **kwargs):

        log_in = ob.getstr('loglevel', 'log_in')  # 日志收集等级
        ch_log_out = ob.getstr('loglevel', 'ch_log_out')  # 控制台输出等级
        fh_log_out = ob.getstr('loglevel', 'fh_log_out')  # 文件输出等级
        save_log = ob.getstr('path', 'save_log')  # 日志文件存储位置
        logger = logging.getLogger('mylog')  # 创建收集器
        logger.setLevel(log_in)  # 设置收入日志的等级
        formatter = logging.Formatter(datefmt='%Y-%m-%d %H:%M:%S', fmt='%(asctime)s-%(filename)s'
                                                                       '-%(levelname)s-%(name)s-日志输出的信息：'
                                                                       '%(message)s')
        now = time.strftime('%Y-%m-%d')  # 获取一下当前的时间
        ch = logging.StreamHandler()  # 创建控制台输出渠道
        ch.setLevel(ch_log_out)  # 设置控制台输出日志等级
        ch.setFormatter(formatter)  # 设置控制台日志输出格式
        logger.addHandler(ch)  # 将控制台输出渠道添加到收集器当中
        try:
            path = os.path.join(save_log, 'log_{}.log'.format(now))  # 设置一下日志的存储路径
            fh = logging.FileHandler(path, 'a', encoding='utf8')  # 创建日志输出到文件的渠道
        except FileNotFoundError:  # 若不存在文件夹创建log文件夹
            os.mkdir(save_log)
            path = os.path.join(save_log, 'log_{}.log'.format(now))  # 设置一下日志的存储路径
            fh = logging.FileHandler(path, 'a', encoding='utf8')  # 创建日志输出到文件的渠道
        fh.setLevel(fh_log_out)  # 设置文件的输出日志等级
        fh.setFormatter(formatter)  # 设置文件的输出格式
        logger.addHandler(fh)  # 将文件输出渠道添加到收集器当中

        return logger
mylog = MyLog()

if __name__ == '__main__':
    mylog = MyLog()
    mylog.debug('debug')
