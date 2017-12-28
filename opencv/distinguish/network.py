"""
network.py
"""
import random

import numpy as np


class Network(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

        self.endbiases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.endweights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        self.rightCount = 0

    def setWB(self, weights, biases):
        self.weights = weights
        self.biases = biases
    def getEnd(self):
        return self.endweights, self.endbiases
    def setEnd(self):
        self.endweights = self.weights
        self.endbiases = self.biases
    def getRightCount(self):
        return self.rightCount
    def setRightCount(self, count):
        self.rightCount = count


    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a


    """
    @param training_data   训练数据 50000个
    @Param epochs          迭代次数
    @Param mini_batch_size 最小训练块
    @Param eta             学习速率
    @Param test_data       测试数据
    """
    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        # zip --> list
        test_data = list(test_data)
        training_data = list(training_data)

        # n_test = 10000
        if test_data: n_test = len(test_data)

        # n = 50000
        n = len(training_data)
        for j in range(epochs):

            # 将序列的所有元素随机排序
            random.shuffle(training_data)

            # 以10个为一组，将training_data分成5000份
            mini_batches = [
                training_data[k:k + mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print(f"Epoch {j}: {self.evaluate(test_data)} / {n_test}")
                if self.getRightCount() < self.evaluate(test_data):
                    self.setRightCount(self.evaluate(test_data))
                    self.setEnd()
            else:
                print(f"Epoch {j} complete")

    def update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            # 计算偏导数，∂Cx/∂blj 和 ∂Cx/∂wljk。
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w - (eta / len(mini_batch)) * nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (eta / len(mini_batch)) * nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        # 初始化
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # 将图像的数值矩阵赋值给activation
        activation = x
        # 使用图像的数值矩阵赋值给activations数组作为第一个元素
        activations = [x]
        #定义装载(z)的容器
        zs = []
        #以下循环会循环网络层数(n) 的n-1次,依次为1-2,2-3，...(n-1)-n
        #其中每次上一层计算出来的结果(activation)会作为下一次计算的输入,依次迭代
        for b, w in zip(self.biases, self.weights):
            #计算z值
            z = np.dot(w, activation) + b
            zs.append(z)
            #S函数计算
            activation = sigmoid(z)
            activations.append(activation)

        #############################反向传播######################################
        #activations[-1]为输出的计算值(可以认为是某一次识别出来的结果)
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return [nabla_b, nabla_w]

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    @staticmethod
    def cost_derivative(output_activations, y):
        return (output_activations - y)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


#计算S函数的导数
def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))
