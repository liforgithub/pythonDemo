#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/21 0021 下午 17:42
# @Author  : 李雪洋
# @File    : dow.py
# @Software: PyCharm
import requests

def getStatus(czkNo):
    url = 'http://www.sinopecsales.com/gas/webjsp/memberOilCardAction_searchCzkStatus.json'
    headers = {
        'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q = 0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'http://www.sinopecsales.com/gas/webjsp/myoil/myOilCard_v1.jsp',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    cookie = dict(
        cookies_are='JSESSIONID=5C778F7FE65B5D83FC6AF92CB785FDF6; HttpOnly=true; \
        Hm_lvt_3a7bd54a4d8be76079e496de5147b070=1511256986; \
        Hm_lpvt_3a7bd54a4d8be76079e496de5147b070=1511256986; \
        province=32; HttpOnly=true; \
        ticket="SSO-550_HV6OP5H8C97J0OIGWW04DTRPY_G6UQQRHIR1URPD56E2O9874C84MLLR9YCJSO,687474703A2F2F31302E352E3138302E35353A383038302F77656273736F"; \
        yunsuo_session_verify=6de4f940941fdb09f2db9c4ad2bb25c4')
    param = {'czkNo': czkNo}
    res = requests.post(url, headers=headers, cookies=cookie, data=param)

    return res.text

cardList = [2510540002396293, 2510540001604564]

for i in cardList:
    print(f"{i} --- {getStatus(i)}")
