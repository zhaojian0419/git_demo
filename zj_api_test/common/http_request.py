"""
============================
Author:赵健
Date:2019-08-30
Time:0:52
E-mail:948883947@qq.com
File:http_request.py
============================

"""
import requests


class HttpRequest(object):
    '''选择是否保留会话请求类'''

    def __init__(self, url, data=None, json=None):
        '''
        初始化
        :param url: 请求地址
        :param data: 请求数据
        '''
        self.url = url
        self.data = data
        self.json = json

    def httprequest(self, method, headers=None, cookies=None):
        '''

        :param method: 方法名（get/post）
        :param headers: 请求头
        :param cookies: cookies
        :return:
        '''

        if method.lower() == 'get':  # 如果方法为get方法
            try:
                response = requests.get(url=self.url, params=self.data,
                                        headers=headers, cookies=cookies)  # 获取响应
                return response  # 返回响应

            except Exception as e:  # 捕获异常
                print("您的get请求发生错误，错误原因{}".format(e))  # 给出用户提示
        elif method.lower() == 'post':  # 如果方法为post方法
            try:
                response = requests.post(url=self.url, data=self.data,
                                         headers=headers, cookies=cookies, json=self.json)  # 获取响应
                return response  # 返回响应
            except Exception as e:  # 捕获异常
                print("您的post请求发生错误，错误原因{}".format(e))  # 给出用户提示
        else:
            print('您的请求方式为{},不是get/post,请核对'.format(method))  # 不是get/post给出用户提示


if __name__ == '__main__':
    url = "http://test.lemonban.com/futureloan/mvc/api/member/login"
    data = {
        "mobilephone": '13331606467',
        "pwd": "123456"
    }
    url1 = "http://test.lemonban.com/futureloan/mvc/api/member/recharge"
    data1 = {
        "mobilephone": '13331606467',
        "amount": 300
    }

    r = HttpRequest(url=url, data=data)
    res = r.httprequest(method='get')

    print(res.json())
    print(res.cookies)
    r1 = HttpRequest(url=url1, data=data1)
    res1 = r1.httprequest(method='get', cookies=res.cookies)
    print(res1.json())
