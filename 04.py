#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
输入某年某月某日，判断这一天是这一年的第几天？
"""

def getday(p, v):
    sum = 0
    for i in range(0, p):
        sum += v[i]
    return sum

def whichday(year, month, day):
    v1 = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    v2 = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
        return getday(month, v2) + day
    else:
        return getday(month, v1) + day

print(whichday(2017, 2, 1))