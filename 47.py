#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 14:30
# @Author  : 李雪洋
# @File    : 47.py
# @Software: PyCharm

"""
两个变量值互换。
"""

x = int(input("请输入X： "))
y = int(input("请输入Y： "))
x, y = y, x

print("x = %d y = %d" % (x, y))