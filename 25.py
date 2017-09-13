#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
求1+2!+3!+...+20!的和。
"""

def getsum(n):
    if n == 1:
        return 1
    else:
        return n * getsum(n - 1)

sum = 0
for i in range(1, 21):
    sum += getsum(i)
print(sum)