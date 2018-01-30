# https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658414051%2Cp_72%3A2039727051%2Cp_6%3AA1AJ19PSB66TGU&page=3&bbn=658414051&ie=UTF8&qid=1515504424

import requests
import re
import html.parser
from pyquery import PyQuery as pq
import pymysql
import pickle
import uuid

# bookList = []
# for i in range(1, 76):
#     print(i)
#     url = f'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658414051%2Cp_72%3A2039727051%2Cp_6%3AA1AJ19PSB66TGU&page={i}&bbn=658414051&ie=UTF8&qid=1515545475'
#     data = requests.get(url).text
#
#     for j in range(0, 16):
#         aa = pq(data)(f"li#result_{(i - 1) * 16 + j}")
#         if str(aa) != '':
#             bookData = pq(aa)
#             # 开始解析数据
#             # 图书封面地址
#             photo_url = bookData('img').attr('src')
#             # 图书的名称
#             book_name = bookData('h2').attr('data-attribute')
#             book_name = html.parser.HTMLParser().unescape(book_name)
#             # 图书作者
#             span_data = bookData('span')
#             span_list = re.findall("<span class=\"a-size-small a-color-secondary\">(.*?)</span>", str(span_data))
#             book_author = span_list[1]
#             # 价格
#             book_price = re.findall("<span class=\"a-size-base a-color-price s-price a-text-bold\">(.*?)</span>",
#                                     str(span_data))
#             book_price = book_price[0]
#             bookList.append({
#                 'photo_url': photo_url,
#                 'book_name': book_name,
#                 'book_author': book_author,
#                 'book_price': book_price
#             })
#
# pickle.dump(bookList, open('./data.pkl', 'wb'))
#
# print(bookList)


def insertData(cursor, db, sql):
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()


data = pickle.load(open('./data.pkl', 'rb'))

# 打开数据库连接
db = pymysql.connect("172.21.3.197", "ehome", "root", "test")
# 使用cursor()方法获取操作游标
cursor = db.cursor()

for d in data:
    # SQL 插入语句
    sql = f"insert into tb_book(id, book_name, book_author, book_photo_url, book_price) values({uuid.uuid1()}, {d['book_name']}, {d['book_author']}, {d['photo_url']}, {d['book_price']})"
    insertData(cursor, db, sql)
    print(d['book_name'])
# 关闭数据库连接
db.close()
