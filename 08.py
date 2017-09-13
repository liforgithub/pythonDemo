#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
输出 9*9 乘法口诀表。

1x1=1
1X2=2 2x2=4

"""

for i in range(1, 10):
    for j in range(1, i + 1):
        print("%dx%d=%d" % (j, i, i * j))

