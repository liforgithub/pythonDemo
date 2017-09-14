#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 14:46
# @Author  : 李雪洋
# @File    : 49.py
# @Software: PyCharm

"""
使用lambda来创建匿名函数。
"""

MAX = lambda x, y: (x > y) * x + (x < y) * y

print(MAX(1, 2))