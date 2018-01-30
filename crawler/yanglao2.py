import urllib.request
import bs4
import re

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'AD_RS_COOKIE=20080917',
    'Host': 'www.stats.gov.cn',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'

req = urllib.request.Request(url, headers=headers)
res = urllib.request.urlopen(req).read()

soup = bs4.BeautifulSoup(res, 'html.parser')

list_province = soup.select(".provincetr")

table = []

# 录取省
for tr in list_province:
    a_list = tr.select('a')
    for a in a_list:
        table.append({
            'children': [],
            'label': a.text,
            'href': a.get('href'),
            'value': ''
        })

# 录取市
for i in range(0, len(table)):

    href = table[i]['href']
    tmpUrl = url + href
    req = urllib.request.Request(tmpUrl, headers=headers)
    res = urllib.request.urlopen(req).read()
    soup = bs4.BeautifulSoup(res, 'html.parser')
    list_city = soup.select(".citytr")
    for city in list_city:
        a_list = city.select('a')
        for ii in range(0, len(a_list), 2):
            table[i]['children'].append({
                'children': [],
                'label': a_list[ii].text,
                'href': a_list[ii].get('href'),
                'value': a_list[ii + 1].text
            })

#录取区
for i in range(0, len(table)):
    for j in range(0, len(table[i]['children'])):
        href = table[i]['children'][j]['href']


print(table)

# tmpCityList = []
# #省
# for href, name in tmpPrivinceList:
#     tmpUrl = url + href
#     req = urllib.request.Request(tmpUrl, headers=headers)
#     res = urllib.request.urlopen(req).read()
#     soup = bs4.BeautifulSoup(res, 'html.parser')
#     list_city = soup.select(".citytr")
#
#     #市
#     for city in list_city:
#         a_list = city.select('a')
#         for i in range(0, len(a_list), 2):
#             href = a_list[i].get('href')
#             num = a_list[i].text
#             name = a_list[i + 1].text
#
#             #区
#             tmpUrl = url + href
#             req = urllib.request.Request(tmpUrl, headers=headers)
#             res = urllib.request.urlopen(req).read()
#             soup = bs4.BeautifulSoup(res, 'html.parser')
#             list_county = soup.select(".countytr")
#
#             for county in list_county:
#                 a_list_2 = county.select('a')
#                 for ii in range(0, len(a_list_2), 2):
#                     county_href = a_list_2[ii].get('href')
#                     county_num = a_list_2[ii].text
#                     county_name = a_list_2[ii + 1].text
#
#                     #
#     break
