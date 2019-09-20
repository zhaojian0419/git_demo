"""
============================
Author:赵健
Date:2019-09-05
Time:23:16
E-mail:948883947@qq.com
File:params_case.py
============================

"""
import re
from common.ob_config import ob


class ConText(object):
    """临时变量类"""
    pass


class Replace(object):
    '''替换用例数据保存到配置文件'''
    def __init__(self, section1=None, section2=None):
        '''
        初始化
        :param section1: 配置文件section1名 默认读取的是临时变量
        :param section2: 配置文件section2名 默认读取的是临时变量
        '''
        self.section1 = section1
        self.section2 = section2


    def replace_data(self, data):

            param1 = '#(.+?)#'  # 匹配规则1
            param2 = '%(.+?)%'  # 匹配规则2

            while re.search(param1, data):  # 如果从data中能匹配的到，循环
                rd1 = re.search(param1, data)  # 匹配到的内容1
                rdata1 = rd1.group()  # 匹配到的要被替换的数据
                key1 = rd1.group(1)  # 获取数据的键
                if self.section1:
                    value1 = ob.getstr(self.section1, key1)  # 获取配置文件存储的值
                else:
                    value1 = getattr(ConText, key1)
                data = data.replace(rdata1, str(value1))  # 替换数据

            while re.search(param2, data):  # 如果从data中能匹配的到，循环
                rd2 = re.search(param2, data)  # 匹配到的内容2
                rdata2 = rd2.group()  # 匹配到的要被替换的数据
                key2 = rd2.group(1)  # 获取数据的键
                if self.section2:
                    value2 = ob.getstr(self.section2, key2)  # 获取配置文件存储的值
                else:
                    value2 = getattr(ConText, key2)
                data = re.sub(rdata2, str(value2), data)  # 替换数据

            return data  # 如果匹配不到直接返回数据

if __name__ == '__main__':
    data = """{
    "mobilephone":"%phone%",
    "pwd":"123456",
    "regname":"zhaojian"
    }"""

    rp = Replace(section2='login')
    data = rp.replace_data(data)
    print(data)



