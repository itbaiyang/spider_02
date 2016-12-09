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
    i += 1
    print(i)
    # print(egg)
    # try:
    #     link_man = re.sub(u"[^\u4e00-\u9fa5]", '', egg['linkman'])
    #     print(link_man)
    #     collection.update({'_id': egg['_id']}, {'$set': {'linkman': link_man}})
    # except:
    #     print('none linkman')

    try:
        list_email = egg['email']
        email = re.sub(u"[\u005d\u2018]", '', list_email)
        collection.update({'_id': egg['_id']}, {'$set': {'email': email}})
    except:
        print('none address')

    # try:
    #     list_tel = egg['tel']
    #     tel = re.sub(u"[\u005d\u2018]", '', list_tel)
    #     collection.update({'_id': egg['_id']}, {'$set': {'tel': tel}})
    # except:
    #     print('none address')
