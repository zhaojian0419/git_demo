"""
============================
Author:赵健
Date:2019-09-15
Time:22:38
E-mail:948883947@qq.com
File:webservice.py
============================

"""
import suds
from suds.client import Client
url1 = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
client1 = Client(url=url1)


data = {
    "uid": "128736687450",
    "pay_pwd": '898989',
    "mobile": "13102445645",
    "cre_id": "220182197403262666",
    "user_name": "成量推",
    "cardid": "6217230302006607441",
    "bank_type": "1001",
    "bank_name": "中国银行"
}

re = client1.service.bindBankCard(data)
print(re)



