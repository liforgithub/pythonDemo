#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
利用条件运算符的嵌套来完成此题：学习成绩>=90分的同学用A表示，60-89分之间的用B表示，60分以下的用C表示。
"""

n = int(input("请输入数字: "))

if not isinstance(n, int) or n <= 0:
        print('请输入一个正确的数字 !')
        exit(0)

print("A" if n >= 90 else ("B" if n >= 60 else "C"))