#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/1/31 0031 上午 11:20
# @Author  : 李雪洋
# @File    : getCounty.py
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


# url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'

def makePkl():
    json = pickle.load(open(PATH, 'rb'))
    try:
        for i in range(0, len(json['children'])):
            if len(json['children'][i]['children']) == 0:
                url = json['children'][i]['href']
                req = urllib.request.Request(url, headers=headers)
                res = urllib.request.urlopen(req, timeout=2).read().decode('gb18030')
                soup = bs4.BeautifulSoup(res, 'html.parser')
                list_county = soup.select(".countytr")

                for county in list_county:
                    a_county_list = county.select('a')
                    if len(a_county_list) > 0:
                        json['children'][i]['children'].append({
                            'children': [],
                            'label': a_county_list[1].text,
                            'href': url[0:url.rindex('/')] + '/' + a_county_list[0].get('href'),
                            'value': a_county_list[0].text
                        })

                # time.sleep(2)
                print(f"{json['label']} - {json['children'][i]['label']}")
                del json['children'][i]['href']
                pickle.dump(json, open(PATH, 'wb'))

    except Exception as e:
        print('异常')
        makePkl()

makePkl()
print('county结束')
