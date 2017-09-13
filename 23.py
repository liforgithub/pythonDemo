#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
打印出如下图案（菱形）:
   *
  ***
 *****
*******
 *****
  ***
   *
"""
lines = 7
middle, lines = int(lines / 2), int(lines / 2) * 2 + 1
for i in range(1, lines + 1):
    empty = abs(i - middle - 1)
    print(' ' * empty, '*' * (2 * (middle - empty) + 1))