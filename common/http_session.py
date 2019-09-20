"""
============================
Author:赵健
Date:2019-08-29
Time:23:18
E-mail:948883947@qq.com
File:http_session.py
============================

"""
from requests import Session


class HttpSession(object):
    """保留会话请求类"""
    session = Session()  # session属性

    def __init__(self, url, data=None, json=None):
        '''
        初始化方法
        :param url: 请求地址
        :param data: 请求数据
        :param json: json格式的请求数据
         '''

        self.url = url  # url属性
        self.data = data  # data属性
        self.json = json  # json属性


    def httprequest(self, method, headers=None):
        '''
        请求方法
        :param method: 方法名（get/post）
        :param headers: 请求头
        :return:
        '''
        if method.lower() == 'get':  # 如果方法为get方法
            try:
                response = self.session.get(url=self.url, params=self.data, headers=headers)  # 获取响应
                return response  # 返回响应
            except Exception as e:  # 捕获异常
                print("您的get请求发生错误，错误原因{}".format(e))  # 给出用户提示
        elif method.lower() == 'post':  # 如果方法为post方法
            try:
                response = self.session.post(url=self.url, data=self.data, headers=headers, json=self.json)  # 获取响应
                return response  # 返回响应
            except Exception as e:  # 捕获异常
                print("您的post请求发生错误，错误原因{}".format(e))   # 给出用户提示
        else:
            print('您的请求方式为{},不是get/post,请核对'.format(method))  # 不是get/post给出用户提示

    def close(self):
        self.session.close()  # 关闭session


if __name__ == '__main__':
    # url = "http://test.lemonban.com/futureloan/mvc/api/member/login"
    # data = {
    #     "mobilephone": '13351514645',
    #     "pwd": "123456"
    # }
    # url1 = "http://test.lemonban.com/futureloan/mvc/api/member/login"
    # data1 = {
    #     "mobilephone": '13331606467',
    #     "pwd": "123456"
    # }
    #
    # r = HttpSession(url=url, data=data)
    # res = r.httprequest(method='post')
    #
    # print(res.json())
    # print(res.cookies)
    # r1 = HttpSession(url=url1, data=data1)
    # res1 = r1.httprequest(method='post')
    # print(res1.json())
    #
    # r1.close()
    url = 'http://test.lemonban.com/futureloan/mvc/api/member/login'
    url1 = 'http://test.lemonban.com/futureloan/mvc/api/loan/add'
    data = {"mobilephone": "13391365850", "pwd": "123456"}
    data1 = {"memberId":0, "title": "借款一年", "amount": 50000, "loanRate": 12, "loanTerm": 12, "loanDateType": 0,
             "repaymemtWay": 5, "biddingDays": 2}
    h = HttpSession(url=url, data=data)
    h.httprequest('post')
    b = HttpSession(url=url1, data=data1)
    c= b.httprequest("post").content.decode('utf8')
    print(c)





