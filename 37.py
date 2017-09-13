#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 0013 下午 17:27
# @Author  : 李雪洋
# @File    : 37.py
# @Software: PyCharm

"""
对10个数进行排序。
"""

v = [2, 3, 4, 1, 8, 5, 6, 7, 9, 0]

# v.sort()
for i in range(9):
    for j in range(i + 1, 10):
        if v[i] > v[j]:
            v[i], v[j] = v[j], v[i]

print(v)