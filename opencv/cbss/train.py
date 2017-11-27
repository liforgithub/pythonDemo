#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/25 0025 下午 14:00
# @Author  : 李雪洋
# @File    : train.py
# @Software: PyCharm

import pickle
import network

training_data, test_data = pickle.load(open('./data.pkl', 'rb'))
# w, b = pickle.load(open('./w-b.pkl', 'rb'))

net = network.Network([900, 30, 26])
# net.setWB(w, b)
net.SGD(training_data, 1000, 20, 3.0, test_data=test_data)
w, b = net.getEnd()
fw = open('./w-b2.pkl', 'wb+')
pickle.dump((w, b), fw)
fw.close()
