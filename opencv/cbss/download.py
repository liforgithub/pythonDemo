#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/8 0008 下午 19:18
# @Author  : 李雪洋
# @File    : download.py
# @Software: PyCharm

# https://hq.cbss.10010.com/image?mode=validate&width=60&height=20&random=0.5718313927110062
import requests

def download(n):

    url = 'http://hq.cbss.10010.com/image?mode=validate&width=60&height=20&random=0.5718313927110062'
    res = requests.get(url, stream=True)
    with open('E:\\pythonDemo\\opencv\\cbss\\img\\' + str(n) + '.bmp', 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    print(n)

for i in range(1, 101):
    download(i)