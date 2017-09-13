#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
利用递归函数调用方式，将所输入的5个字符，以相反顺序打印出来。
"""

def rev(s, n):
    if (n >= len(s) - 1 - n):
        return ''.join(s)
    s[n], s[len(s) - 1 - n] = s[len(s) - 1 - n], s[n]
    return rev(s, n + 1)

print(rev(list(input("请输入五个字符: ")), 0))