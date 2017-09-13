#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 0013 下午 15:54
# @Author  : 李雪洋
# @File    : 28.py
# @Software: PyCharm

"""
有5个人坐在一起，
问第五个人多少岁？他说比第4个人大2岁。
问第4个人岁数，他说比第3个人大2岁。
问第三个人，又说比第2人大两岁。
问第2个人，说比第一个人大两岁。
最后问第一个人，他说是10岁。
请问第五个人多大？
"""

def getage(deep):
    if deep == 1: return 10
    return getage(deep - 1) + 2

print(getage(5))
