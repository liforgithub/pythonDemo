#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 0013 下午 17:14
# @Author  : 李雪洋
# @File    : 36.py
# @Software: PyCharm

"""
求100之内的素数。
"""

import math

def prime(n):
    c = int(math.sqrt(n)) + 1
    for j in range(2, c):
        if n % j == 0:
            return False
    return print(n)

for i in range(3, 101, 2):
    prime(i)