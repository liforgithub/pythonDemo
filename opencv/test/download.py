#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/10 0010 下午 15:22
# @Author  : 李雪洋
# @File    : download.py
# @Software: PyCharm

# https://passport.fenqile.com/getimage?r=0.2788527577112494
import requests

def download(n):

    url = 'https://passport.fenqile.com/getimage?r=0.2788527577112494'
    res = requests.get(url, stream=True)
    with open('E:\\pythonDemo\\opencv\\test\\img\\' + str(n) + '.bmp', 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    print(n)

for i in range(1, 101):
    download(i)