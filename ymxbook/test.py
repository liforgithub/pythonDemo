#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/1/10 0010 下午 13:37
# @Author  : 李雪洋
# @File    : test.py
# @Software: PyCharm
import pickle
import uuid

data = pickle.load(open('./data.pkl', 'rb'))

for d in data:
    print(d['photo_url'])