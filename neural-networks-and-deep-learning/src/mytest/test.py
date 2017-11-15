#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/25 0025 下午 14:00
# @Author  : 李雪洋
# @File    : test.py
# @Software: PyCharm

import pickle
import numpy as np
from decimal import Decimal
import cv2


# training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

# tr = []
# for (x, y) in validation_data:
#     print(x)
#     tr = x
#     print(y)
#     break

# net = network.Network([784, 30, 10])
# net.SGD(training_data, 30, 10, 3.0, test_data=test_data)
# w, b = net.getEnd()
# print(w)
# print(net.getRightCount())
# #
# fw = open('./w.pkl', 'wb+')
# fb = open('./b.pkl', 'wb+')
# pickle.dump(w, fw)
# pickle.dump(b, fb)
# fw.close()
# fb.close()


# for (x, y) in test_data:
#     print(x)
#     print(y)
#     break


def sigmoid(z):
    """The sigmoid function."""
    return 1.0 / (1.0 + np.exp(-z))


def feedforward(a):
    """Return the output of the network if ``a`` is input."""
    biases = pickle.load(open('./b.pkl', 'rb'))
    weights = pickle.load(open('./w.pkl', 'rb'))
    for b, w in zip(biases, weights):
        a = sigmoid(np.dot(w, a) + b)
    return a


card = [4, 1, 3, 0, 2, 6, 1, 9, 9, 2, 1, 2, 2, 7, 5, 7, 1, 3]
n = 0
pkllist = []
for i in range(1, 37):
    srcImg = cv2.imread(f'./tmp/{i}.bmp', 0)
    gray = cv2.equalizeHist(srcImg)
    cv2.imshow('equalizeHist', gray)
    cv2.waitKey(0)

    array = np.array(gray)  # array is a numpy array
    print(array)
    cv2.waitKey(0)
    ary = []
    for x in array:
        for y in x:
            aa = [float(Decimal((255 - y) / 255).quantize(Decimal('0.00000000')))]
            ary.append(aa)
    if n == len(card):
        n = 0
    print(card[n])
    pkllist.append((ary, card[n]))
    n += 1
fw = open('./data.pkl', 'wb+')
pickle.dump(pkllist, fw)

data = pickle.load(open('./data.pkl', 'rb'))
for x, y in data:
    print(y)


# print(ary)
# print(f"n = {np.argmax(feedforward(ary))}")
