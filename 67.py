#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 15:59
# @Author  : 李雪洋
# @File    : 67.py
# @Software: PyCharm

"""
输入数组，最大的与第一个元素交换，最小的与最后一个元素交换，输出数组。
"""

v = [3, 4, 1, 55, 7, 44, 8, 5]

for i in range(0, len(v)):
    if v[i] == max(v):
        v[0], v[i] = v[i], v[0]
for i in range(0, len(v)):
    if v[i] == min(v):
        v[len(v) - 1], v[i] = v[i], v[len(v) - 1]
print(v)