#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 15:19
# @Author  : 李雪洋
# @File    : 61.py
# @Software: PyCharm

"""
打印出杨辉三角形（要求打印出10行如下图）
1
1 1
1 2 1
1 3 3 1
1 4 6 4 1
1 5 10 10 5 1
1 6 15 20 15 6 1
1 7 21 35 35 21 7 1
1 8 28 56 70 56 28 8 1
1 9 36 84 126 126 84 36 9 1
"""

n = 10

v = []
for i in range(2, n + 1):
    k = []
    for j in range(0, len(v)):
        if j == 0:
            k.append(1)
        else:
            k.append(v[j - 1] + v[j])
    k.append(1)
    v = k
    print(k)

