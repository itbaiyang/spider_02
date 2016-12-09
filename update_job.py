#!/usr/bin/python

from pymongo import MongoClient

client = MongoClient()
db = client.spider_02
collection = db.job_51_u
position = collection.find().skip(95649)
i = 95649
for item in position:
    print(item["link"])
    update = eval(item["position"])
    collection.update({"link": item["link"]}, {"$set": {"position": update}})
    print(i)
    i += 1
