#!/usr/bin/python

import socket
import http.client
import re
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client.spider_02
collection = db.yingcai_wfq

i = 0
for egg in collection.find():
    i += 1
    print(i)
    # print(egg)
    try:
        link_man = re.sub(u"[^\u4e00-\u9fa5]", '', egg['linkman'])
        print(link_man)
        collection.update({'_id': egg['_id']}, {'$set': {'linkman': link_man}})
    except:
        print('none linkman')

    # try:
    #     list_address = egg['address']
    #     address = re.sub(u"[\u005d\u2018]", '', list_address)
    #     collection.update({'_id': egg['_id']}, {'$set': {'address': address}})
    # except:
    #     print('none address')
    # list_address = egg['address']
    # address = re.sub(u"[\u005d\u2018]", '', list_address)
    # collection.update({'_id': egg['_id']}, {'$set': {egg['linkman']: link_man, egg['address']: address}})


