#https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658414051%2Cp_72%3A2039727051%2Cp_6%3AA1AJ19PSB66TGU&page=3&bbn=658414051&ie=UTF8&qid=1515504424

import requests
import re
import html.parser




def download():

    url = 'https://www.amazon.cn/s/ref=s9_acsd_al_bw_clnk_r?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&rh=i%3Astripbooks%2Cn%3A658390051%2Cn%3A%21658391051%2Cn%3A658414051%2Cp_72%3A2039727051%2Cp_6%3AA1AJ19PSB66TGU&bbn=658414051&rw_html_to_wsrp=1&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=merchandised-search-6&pf_rd_r=B14Z9S0C3GHV4THZV3J2&pf_rd_t=101&pf_rd_p=2c14481d-ba56-4259-891a-8360809a970e&pf_rd_i=658414051'
    res = requests.get(url)
    data = re.findall("<a class=\"a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal\" target=\"_blank\" title=\"(.*?)\"", res.text)

    for d in data:
        print(html.parser.HTMLParser().unescape(d))

download()