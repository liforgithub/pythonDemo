#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/17 0017 上午 9:43
# @Author  : 李雪洋
# @File    : app.py
# @Software: PyCharm

from flask import *
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/user', methods=['POST'])
def adduser():
    return jsonify({'task': request.form.get('user')}), 201

@app.route('/getList', methods=['GET'])
def getList():
    data = pickle.load(open('./data.pkl', 'rb'))
    return jsonify({'list': data}), 200

if __name__ == '__main__':
    app.run(debug=True)