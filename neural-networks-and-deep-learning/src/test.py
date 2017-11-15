#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/25 0025 下午 14:00
# @Author  : 李雪洋
# @File    : test.py
# @Software: PyCharm

import network
import mnist_loader

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
# net = network.Network([784, 30, 10])
# net.SGD(training_data, 30, 10, 3.0, test_data=test_data)
for x, y in training_data:
    print(x)
    print('---------------')
    print(y)
    break