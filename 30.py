#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 0013 下午 16:23
# @Author  : 李雪洋
# @File    : 30.py
# @Software: PyCharm

"""
一个5位数，判断它是不是回文数。即12321是回文数，个位与万位相同，十位与千位相同。
"""

def compare(s, n):
    if n >= len(s) - 1 - n:
        return print("是回文数")
    elif s[n] != s[len(s) - 1 - n]:
        return print("不是回文数")
    else:
        return compare(s, n + 1)


compare(list(input("请输入一个5位数: ")), 0)