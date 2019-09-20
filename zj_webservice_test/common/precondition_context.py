"""
============================
Author:赵健
Date:2019-09-11
Time:22:53
E-mail:948883947@qq.com
File:precondition_context.py
============================

"""
import  suds
from suds.client import Client
from common.ob_config import ob
from common.ob_mysql import ObMysql
from common.params_case import ConText
from common.random_mobile import update_phone

class PreClass(object):
    '''前置条件类'''
    def sendMCode(self):
        mysql = ObMysql(database="sms_db_45")
        url = "http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl"
        client = Client(url=url)  # 建立连接
        client_ip = ob.getstr('register', 'client_ip')
        phone = ob.getstr('register', 'phone')
        username = ob.getstr('register', 'username')
        pwd = ob.getstr('register', 'pwd')
        data = {
                 "client_ip":client_ip,
                 "tmpl_id": 1,
                 "mobile": phone
                }
        client.service.sendMCode(data) # 请求
        verify_code = mysql.select("SELECT Fverify_code FROM t_mvcode_info_6 WHERE Fmobile_no= '{}'"
                                   .format(phone))[0][0]  # 获取短信验证码
        setattr(ConText, 'client_ip', client_ip)  # 将ip地址添加到临时变量
        setattr(ConText, 'phone', phone)  # 将手机号添加到临时变量
        setattr(ConText, 'username', username)  # 将用户名添加到临时变量
        setattr(ConText, 'pwd', pwd)  # 密码添加到临时变量
        setattr(ConText, 'verify_code', verify_code)  # 将短信验证码添加到临时变量
        mysql.close()
        update_phone()  # 更新配置文件

    def userRegister(self):
        '''注册方法'''
        self.sendMCode()  # 发送短信验证码
        mysql = ObMysql('user_db')
        url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
        verify_code = getattr(ConText, 'verify_code')
        user_id = getattr(ConText, 'username')
        pwd = getattr(ConText, 'pwd')
        mobile = getattr(ConText, 'phone')
        ip = getattr(ConText, 'client_ip')
        data = {
            "verify_code": verify_code,
            "user_id": user_id,
            "channel_id": 1,
            "pwd": pwd,
            "mobile": mobile,
            "ip": ip
        }
        client = Client(url=url)  # 建立连接
        client.service.userRegister(data)  # 发送请求
        uid = mysql.select("SELECT Fuid FROM t_user_info WHERE Fuser_id= '{}'".format(user_id))[0][0]
        setattr(ConText, 'uid', uid)  # 将uid写进临时变量
        mysql.close()





if __name__ == "__main__":
    pr = PreClass()
    pr.userRegister()
    re = getattr(ConText, 'uid')
    print(re)
