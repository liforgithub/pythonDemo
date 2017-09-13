#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
斐波那契数列（Fibonacci sequence），又称黄金分割数列，指的是这样一个数列：0、1、1、2、3、5、8、13、21、34、……。

F0 = 0
F1 = 1
F2 = F0 + F1
.
.
.
Fn = F(n-2) + F(n-1)(n>=2)
"""

def fib(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    if n >=3:
        return fib(n-2) + fib(n-1)

for i in range(1, 11):
    print(fib(i))

# print(fib(int(input("请输入层数: "))))