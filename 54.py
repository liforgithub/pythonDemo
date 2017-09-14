#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 14:58
# @Author  : 李雪洋
# @File    : 54.py
# @Software: PyCharm

"""
取一个整数a从右端开始的4〜7位。
9 ------ 1001
"""
a = 9
b = a >> 4
c = ~(~0 << 4)
d = b & c
print('%o\t%o' % (a, d))