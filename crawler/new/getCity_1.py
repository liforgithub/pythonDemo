#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/1/31 0031 上午 11:16
# @Author  : 李雪洋
# @File    : getCity.py
# @Software: PyCharm

import urllib.request
import bs4
import re
import time
import pickle
import configparser

cf = configparser.ConfigParser()
cf.read("config.conf", encoding='utf-8')

PATH = cf.get('path', 'PATH')

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'AD_RS_COOKIE=20080919',
    'Host': 'www.stats.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.113 Safari/537.36'
}
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'

json = pickle.load(open(PATH, 'rb'))

href = json['href']
tmpUrl = url + href
req = urllib.request.Request(tmpUrl, headers=headers)
res = urllib.request.urlopen(req).read().decode('gb18030')
soup = bs4.BeautifulSoup(res, 'html.parser')
list_city = soup.select(".citytr")
for city in list_city:
    a_list = city.select('a')
    for ii in range(0, len(a_list), 2):
        json['children'].append({
            'children': [],
            'label': a_list[ii + 1].text,
            'href': url + a_list[ii].get('href'),
            'value': a_list[ii].text
        })
del json['href']
pickle.dump(json, open(PATH, 'wb'))

print('city结束')