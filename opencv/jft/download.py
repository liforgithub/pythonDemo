#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/8 0008 下午 19:18
# @Author  : 李雪洋
# @File    : download.py
# @Software: PyCharm

#https://www.jft.net.cn:4433/NewMember/memberAct/userDo/getCheckCodeImage.jsp?type=cardLogin&nowtime=1511783584031
import requests

def download(n):

    url = 'https://www.jft.net.cn:4433/NewMember/memberAct/userDo/getCheckCodeImage.jsp?type=cardLogin&nowtime=1511783584031'
    res = requests.get(url, stream=True)
    with open('E:\\pythonDemo\\opencv\\jft\\img\\' + str(n) + '.bmp', 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    print(n)

for i in range(1, 101):
    download(i)