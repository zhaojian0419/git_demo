"""
============================
Author:赵健
Date:2019-08-25
Time:15:58
E-mail:948883947@qq.com
File:mylog.py
============================

"""
import logging
import time
import os
import common.constants as cons  # 导入常量模块
from common.ob_config import ob


class MyLog(object):
    '''日志类'''
    log_in = ob.getstr('loglevel', 'log_in')  # 日志收集等级
    ch_log_out = ob.getstr('loglevel', 'ch_log_out')  # 控制台输出等级
    fh_log_out = ob.getstr('loglevel', 'fh_log_out')  # 文件输出等级
    save_log = cons.LOGS_DIR  # 日志文件存储位置

    def __init__(self, logname):
        '''
        初始化
        :param logname: 收集器的名字
        '''
        self.logname = logname


    def mylog(self, level, msg):
        '''
        日志方法
        :param level: 输出的等级
        :param msg: 输出的信息
        :return:
        '''

        logger = logging.getLogger(self.logname)  # 创建收集器
        logger.setLevel(self.log_in)  # 设置收入日志的等级
        formatter = logging.Formatter(datefmt='%Y-%m-%d %H:%M:%S', fmt='%(asctime)s-[%(filename)s-->line:%(lineno)d]'
                                                                       '-%(levelname)s-%(name)s-日志输出的信息：'
                                                                       '%(message)s')
        now = time.strftime('%Y-%m-%d')  # 获取一下当前的时间
        ch = logging.StreamHandler()  # 创建控制台输出渠道
        ch.setLevel(self.ch_log_out)  # 设置控制台输出日志等级
        ch.setFormatter(formatter)  # 设置控制台日志输出格式
        logger.addHandler(ch)  # 将控制台输出渠道添加到收集器当中
        try:
            path = os.path.join(self.save_log, 'log_{}.log'.format(now))  # 设置一下日志的存储路径
            fh = logging.FileHandler(path, 'a', encoding='utf8')  # 创建日志输出到文件的渠道
        except FileNotFoundError:  # 若不存在文件夹创建log文件夹
            os.mkdir(self.save_log)
            path = os.path.join(self.save_log, 'log_{}.log'.format(now))  # 设置一下日志的存储路径
            fh = logging.FileHandler(path, 'a', encoding='utf8')  # 创建日志输出到文件的渠道
        fh.setLevel(self.fh_log_out)  # 设置文件的输出日志等级
        fh.setFormatter(formatter)  # 设置文件的输出格式
        logger.addHandler(fh)  # 将文件输出渠道添加到收集器当中

        if level == 'DEBUG':  # 如果输出日志等级等于DEBUG调用debug输出方法
            logger.debug(msg)
        elif level == 'INFO':  # 如果输出日志等级等于INFO调用info输出方法
            logger.info(msg)
        elif level == 'WARNING':  # 如果输出日志等级等于WARNING调用warning输出方法
            logger.warning(msg)
        elif level == 'ERROR':  # 如果输出日志等级等于ERROR调用error输出方法
            logger.error(msg)
        elif level == 'CRITICAL':  # 如果输出日志等级等于CRITICAL调用critical输出方法
            logger.critical(msg)

        logger.removeHandler(ch)  # 回收控制台渠道
        logger.removeHandler(fh)  # 回收文件渠道

    def debug(self, msg):
        '''
        debug方法
        :param msg: 输出的内容
        :return:
        '''
        self.mylog("DEBUG", msg)

    def info(self, msg):
        '''
        info方法
        :param msg: 输出的内容
        :return:
        '''
        self.mylog('INFO', msg)

    def warning(self, msg):
        '''
        warning 方法
        :param msg: 输出的内容
        :return:
        '''
        self.mylog('WARNING', msg)

    def error(self, msg):
        '''
        error方法
        :param msg: 输出的内容
        :return:
        '''
        self.mylog("ERROR", msg)

    def critical(self, msg):
        '''
        critical方法
        :param msg: 输出的内容
        :return:
        '''
        self.mylog('CRITICAL', msg)


if __name__ == '__main__':
    ml = MyLog('mylog')
    ml.error('警告')
