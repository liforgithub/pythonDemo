#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
利用递归方法求5!。
"""

def getsum(n):
    if n == 1:
        return 1
    else:
        return n * getsum(n - 1)

print(getsum(5))