#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 上午 8:59
# @Author  : 李雪洋
# @File    : 39.py
# @Software: PyCharm

"""
有一个已经排好序的数组。现输入一个数，要求按原来的规律将它插入数组中。
"""

v = [1, 3, 7, 16, 22, 35, 40, 56, 78, 90]

pt = int(input("请输入一个数: "))

for i in range(0, len(v) - 2):
    if v[i] > v[i + 1]:
        if v[i] <= pt:
            v.insert(i, pt)
            break
        elif v[i] >= pt >= v[i + 1]:
            v.insert(i + 1, pt)
            break
        elif v[i + 1] >= pt:
            v.append(pt)
            break
    else:
        if v[i] >= pt:
            v.insert(i, pt)
            break
        elif v[i] <= pt <= v[i + 1]:
            v.insert(i + 1, pt)
            break
        elif v[i + 1] <= pt:
            v.append(pt)
            break
print(v)

