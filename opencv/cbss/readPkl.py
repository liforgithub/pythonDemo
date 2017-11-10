#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/9 0009 下午 16:49
# @Author  : 李雪洋
# @File    : readPkl.py
# @Software: PyCharm
import pickle
from numpy import *

data, test = pickle.load(open('./data.pkl', 'rb'))

print(test[0])