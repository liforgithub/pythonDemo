#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/10 0010 下午 12:43
# @Author  : 李雪洋
# @File    : 03.py
# @Software: PyCharm

from urllib import request, parse
import json

try:

    url = 'http://fanyi.baidu.com/sug'
    formData = {}
    formData['kw'] = '南京'

    param = parse.urlencode(formData).encode('utf-8')

    res = request.urlopen(url, param)

    if res.getcode() != 200:
        print("页面返回失败")
    data = res.read().decode('unicode_escape')

    jsonObj = json.loads(data)

    for i in jsonObj['data']:
        print(i['k'] + " : " + i['v'])

except Exception as e:
    print(e)
finally:
    print("结束")