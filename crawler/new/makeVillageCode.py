#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/2/2 0002 上午 10:13
# @Author  : 李雪洋
# @File    : makeVillageCode.py
# @Software: PyCharm
import urllib.request
import bs4
import re

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

json = {}

"""
获取省份数据
"""


def getProvinceInfo():
    try:
        provinceList = []
        req = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(req, timeout=1).read()

        soup = bs4.BeautifulSoup(res, 'html.parser')

        list_province = soup.select(".provincetr")

        # 录取省
        for tr in list_province:
            a_list = tr.select('a')
            for a in a_list:
                provinceList.append({
                    'children': [],
                    'label': a.text,
                    'href': a.get('href'),
                    'value': ''
                })
                print(a.text)
        return provinceList
    except Exception as e:
        print('获取省份异常, 重新获取')
        getProvinceInfo()


"""
获取市级数据
"""


def getCityInfo():
    try:
        href = json['href']
        json['children'] = []
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
    except Exception as e:
        print('获取市级异常, 重新获取')
        getCityInfo()


"""
获取区级数据
"""


def getCountyInfo():
    try:
        for i in range(0, len(json['children'])):
            if len(json['children'][i]['children']) == 0:
                tmpUrl = json['children'][i]['href']
                req = urllib.request.Request(tmpUrl, headers=headers)
                res = urllib.request.urlopen(req, timeout=1).read().decode('gb18030')
                soup = bs4.BeautifulSoup(res, 'html.parser')
                list_county = soup.select(".countytr")

                for county in list_county:
                    a_county_list = county.select('a')
                    if len(a_county_list) > 0:
                        json['children'][i]['children'].append({
                            'children': [],
                            'label': a_county_list[1].text,
                            'href': tmpUrl[0:tmpUrl.rindex('/')] + '/' + a_county_list[0].get('href'),
                            'value': a_county_list[0].text
                        })

                # time.sleep(2)
                print(f"{json['label']} - {json['children'][i]['label']}")
                del json['children'][i]['href']
    except Exception as e:
        print('获取区级异常, 重新获取')
        getCountyInfo()


"""
获取街道数据
"""


def getTowerInfo():
    try:
        for city_index in range(0, len(json['children'])):
            for county_index in range(0, len(json['children'][city_index]['children'])):
                if len(json['children'][city_index]['children'][county_index]['children']) == 0:
                    tmpUrl = json['children'][city_index]['children'][county_index]['href']
                    req = urllib.request.Request(tmpUrl, headers=headers)

                    res = urllib.request.urlopen(req, timeout=1).read().decode('gb18030')
                    soup = bs4.BeautifulSoup(res, 'html.parser')
                    list_towntr = soup.select(".towntr")
                    for towntr in list_towntr:
                        a_list_tower = towntr.select('a')
                        if len(a_list_tower) > 0:
                            json['children'][city_index]['children'][county_index]['children'].append({
                                'children': [],
                                'label': a_list_tower[1].text,
                                'href': tmpUrl[0:tmpUrl.rindex('/')] + '/' + a_list_tower[0].get('href'),
                                'value': a_list_tower[0].text
                            })

                    del json['children'][city_index]['children'][county_index]['href']
                    print(
                        f"{json['label']} - {json['children'][city_index]['label']} - {json['children'][city_index]['children'][county_index]['label']}")
    except Exception as e:
        print('获取街道异常, 重新获取')
        getTowerInfo()


"""
获取社区数据
"""


def getVillageInfo():
    try:
        for city_index in range(0, len(json['children'])):
            for county_index in range(0, len(json['children'][city_index]['children'])):
                for tower_index in range(0, len(json['children'][city_index]['children'][county_index]['children'])):
                    if len(json['children'][city_index]['children'][county_index]['children'][tower_index][
                               'children']) == 0:
                        tmpUrl = json['children'][city_index]['children'][county_index]['children'][tower_index]['href']
                        req = urllib.request.Request(tmpUrl, headers=headers)

                        res = urllib.request.urlopen(req, timeout=1).read().decode('gb18030')
                        soup = bs4.BeautifulSoup(res, 'html.parser')
                        list_towntr = soup.select(".villagetr")
                        for towntr in list_towntr:
                            td_list_tower = towntr.select('td')
                            if len(td_list_tower) > 0:
                                json['children'][city_index]['children'][county_index]['children'][tower_index]['children'].append({
                                    'label': td_list_tower[2].text,
                                    'value': td_list_tower[0].text
                                })

                        del json['children'][city_index]['children'][county_index]['children'][tower_index]['href']
                        print(
                            f"{json['label']} - {json['children'][city_index]['label']} - {json['children'][city_index]['children'][county_index]['label']} - {json['children'][city_index]['children'][county_index]['children'][tower_index]['label']}")
    except Exception as e:
        print('获取社区异常, 重新获取')
        getVillageInfo()


provinceList = getProvinceInfo()
for pro in provinceList:
    json = pro
    fileName = f"./complete/{pro['label']}.json"
    getCityInfo()
    getCountyInfo()
    getTowerInfo()
    getVillageInfo()
    source = str(json)
    source = re.sub(r"'children'", "children", source)
    source = re.sub(r"'label'", "label", source)
    source = re.sub(r"'value'", "value", source)
    f = open(fileName, 'w', encoding='utf8')
    f.write(source)
    f.flush()
    f.close()
