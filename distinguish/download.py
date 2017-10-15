#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/12 0012 上午 10:52
# @Author  : 李雪洋
# @File    : download.py
# @Software: PyCharm

import requests

def download(n):

    url = 'http://119.39.227.91:8108/tbss/checkCodeController/getCheckCode.do'
    res = requests.get(url, stream=True)
    with open('D:\\python_pro\\pythonDemo\\distinguish\\img\\' + str(n) + '.bmp', 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()

for i in range(1, 101):
    download(i)