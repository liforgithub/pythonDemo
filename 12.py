#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
判断101-200之间有多少个素数，并输出所有素数
"""

import math

def isPrime(n):
    loop = 1
    k = int(math.sqrt(n + 1))
    for i in range(2, k+1):
        if n % i == 0:
            loop = 0
            break
    if loop == 1:
        print(n)

for i in range(101, 201):
    isPrime(i)