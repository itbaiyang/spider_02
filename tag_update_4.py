#!/usr/bin/python

from pymongo import MongoClient

client = MongoClient()
db = client.spider_02
collection = db.job
position = collection.find({"company_tag": {"$exists": True}}).skip(600000)
i = 600000
for item in position:
    print(item["company_name"])
    update = eval(item["company_tag"])
    collection.update({"company_name": item["company_name"]}, {"$set": {"company_tag": update}})
    print(i)
    i += 1