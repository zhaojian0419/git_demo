"""
============================
Author:赵健
Date:2019-09-10
Time:23:33
E-mail:948883947@qq.com
File:precondition_conf.py
============================

"""
from le_python自动化.zj_apt_test.common.http_session import HttpSession
from le_python自动化.zj_apt_test.common.ob_config import ob
from le_python自动化.zj_apt_test.common.random_mobile import update_phone
from le_python自动化.zj_apt_test.common.ob_mysql import ObMysql


class PreClass(object):
    '''前置条件类'''
    mysql = ObMysql()

    def register(self):
        '''注册'''
        url = "http://test.lemonban.com/futureloan/mvc/api/member/register"
        phone = ob.getstr('register', 'phone')
        pwd = ob.getstr('register', 'pwd')
        data = {
            "mobilephone": phone,
            "pwd": pwd,
            "regname": "zhaojian"
        }
        HttpSession(url=url, data=data).httprequest(method='post')  # 发送请求

        ob.write('login', 'phone', phone)  # 将注册之后的手机号码写到配置文件当中
        ob.write('login', 'pwd', pwd)  # 将注册之后的密码写到配置文件当中
        memerid = self.mysql.select('SELECT id FROM member WHERE MobilePhone="{}"'.
                                    format(ob.getstr('login', 'phone')))[0][0]
        ob.write('login', 'memberid', str(memerid))  # 将注册之后的用户id写到配置文件当中
        update_phone()  # 更新配置文件的手机号码

    def login(self):
        '''登录'''
        self.register()  # 注册
        url = "http://test.lemonban.com/futureloan/mvc/api/member/login"
        phone = ob.getstr('login', 'phone')
        pwd = ob.getstr('login', 'pwd')
        data = {
            "mobilephone": phone,
            "pwd": pwd
        }
        HttpSession(url=url, data=data).httprequest(method='post')  # 发送请求

    def recharge(self, amount=10000):
        '''
        充值
        :param amount: 充值金额
        :return:
        '''
        self.login()  # 登录
        url = "http://test.lemonban.com/futureloan/mvc/api/member/recharge"
        phone = ob.getstr('login', 'phone')
        data = {
            "mobilephone": phone,
            "amount": amount
        }
        HttpSession(url=url, data=data).httprequest(method='post')  # 发送请求

    def withdraw(self, r_amount=10000, w_amount=5000):
        '''
        取现
        :param r_amount: 充值金额
        :param w_amount: 取现金额
        :return:
        '''
        self.recharge(r_amount)  # 先充值
        url = "http://test.lemonban.com/futureloan/mvc/api/member/withdraw"
        phone = ob.getstr('login', 'phone')
        data = {
            "mobilephone": phone,
            "amount": w_amount
        }
        HttpSession(url=url, data=data).httprequest(method='post')  # 发送请求

    def add(self, title='加标', amount=10000, loanrate=18.0, loanterm=6,
            loandatetype=0, repaymemtway=4, biddingdays=5):
        '''
        加标
        :param title:标题
        :param amount:借款金额
        :param loanrate:年利率
        :param loanterm:借款期限
        :param loandatetype:借款期限类型
        :param repaymemtway:还款方式
        :param biddingdays:竞标天数
        :return:
        '''
        self.recharge()
        url = "http://test.lemonban.com/futureloan/mvc/api/loan/add"
        memerid = ob.getint('login', 'memberid')
        data = {
            "memberId": memerid,
            "title": title,
            "amount": amount,
            "loanRate": loanrate,
            "loanTerm": loanterm,
            "loanDateType": loandatetype,
            "repaymemtWay": repaymemtway,
            "biddingDays": biddingdays
        }
        HttpSession(url=url, data=data).httprequest(method='post')  # 发送请求
        loanid = self.mysql.select('SELECT id FROM loan WHERE MemberId = "{}"'.
                                   format(memerid))[0][0]
        ob.write('login', 'loanid', loanid)    # 将标id写进配置文件


pr = PreClass()
id =pr.add()
print(id)
