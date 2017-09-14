#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 16:15
# @Author  : 李雪洋
# @File    : 69.py
# @Software: PyCharm

"""
有n个人围成一圈，顺序排号。从第一个人开始报数（从1到3报数），凡报到3的人退出圈子，问最后留下的是原来第几号的那位
"""

v = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

isContinue = True
cnt = 0
while isContinue:
    i = 0
    for i in range(0, len(v)):
        if v[i] == 1:
            cnt += 1
            if cnt == 3:
                v[i] = 0
                cnt = 0
    print(v)
    if v.count(1) == 1:
        print("最后一个是 %d" % v.index(1))
        isContinue = False