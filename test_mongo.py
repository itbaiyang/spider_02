#!/usr/bin/python

import socket
import http.client
import re
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client.spider_02
collection = db.yingcai

i = 0
for egg in collection.find():
    # 26075
    i += 1
    print(i)
    list_gg = egg['detail']
    if list_gg == '[]':
        print(list_gg)
    else:
        list_u = re.sub(u"[\u2022]", '', list_gg)
        list_arr = list_u.split('\',')
        for item in list_arr:
            item_arr = item.split('：')
            key = re.sub(u"[^\u4e00-\u9fa5]", '', item_arr[0])
            # value = re.sub(u"[^\u0030-\u0039\u002d\u4e00-\u9fa5]", '', )
            value = str(item_arr[1])
            # print('key', key)
            # print('value', item_arr[1])
            # print(key, value)
            collection.update({'_id': egg['_id']}, {'$set': {key: value}})


