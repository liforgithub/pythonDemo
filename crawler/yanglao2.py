import urllib.request
import bs4
import re
import time
import pickle

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

req = urllib.request.Request(url, headers=headers)
res = urllib.request.urlopen(req).read()

soup = bs4.BeautifulSoup(res, 'html.parser')

list_province = soup.select(".provincetr")

table = pickle.load(open('./data.pkl', 'rb'))

if len(table) == 0:
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
                    'label': a_list[ii + 1].text,
                    'href': a_list[ii].get('href'),
                    'value': a_list[ii].text
                })
    pickle.dump(table, open('./data.pkl', 'wb'))

# 录取区
for i in range(0, len(table)):
    for j in range(0, len(table[i]['children'])):
        if len(table[i]['children'][j]['children']) == 0:
            href = table[i]['children'][j]['href']
            tmpUrl = url + href
            req = urllib.request.Request(tmpUrl, headers=headers)
            res = urllib.request.urlopen(req).read()
            soup = bs4.BeautifulSoup(res, 'html.parser')
            list_county = soup.select(".countytr")
            for county in list_county:
                a_county_list = county.select('a')
                if len(a_county_list) > 0:
                    table[i]['children'][j]['children'].append({
                        'children': [],
                        'label': a_county_list[1].text,
                        'href': href[0:href.index('.')] + '/' + a_county_list[0].get('href'),
                        'value': a_county_list[0].text
                    })

            # time.sleep(2)
            print(f"{table[i]['label']} - {table[i]['children'][j]['label']}")
            pickle.dump(table, open('./data.pkl', 'wb'))

print(table)


