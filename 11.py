#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
古典问题：有一对兔子，从出生后第3个月起每个月都生一对兔子，小兔子长到第三个月后每个月又生一对兔子，假如兔子都不死，问每个月的兔子总数为多少？

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
    if n >= 3:
        return fib(n-1) + fib(n-2)

print(fib(36))