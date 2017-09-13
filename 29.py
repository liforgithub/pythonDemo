#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 0013 下午 16:09
# @Author  : 李雪洋
# @File    : 29.py
# @Software: PyCharm

"""
给一个不多于5位的正整数，要求：一、求它是几位数，二、逆序打印出各位数字。
"""

def count(n):
    i = 0
    for i in range(1, 6):
        if int(n / 10) > 0:
            i += 1
            n /= 10
        else:
            return i

def rev(s, n):
    if n >= len(s)-1-n:
        return s
    s[n], s[len(s) - 1 - n] = s[len(s) - 1 - n], s[n]
    return rev(s, n + 1)

str = input("请输入一个不多于5位的正整数： ")
s = int(str)
print("%d位数" % count(s))
print("逆序： %d" % int("".join(rev(list(str), 0))))