#!/usr/bin/python

from pymongo import MongoClient

client = MongoClient()
db = client.spider_02
collection = db.job_51_u
position = collection.find()
i = 1
for item in position:
    # print(item["link"])
    try:
        update = eval(item["position"])
        collection.update({"link": item["link"]}, {"$set": {"position": update}})
    except:
        print("done")
    i += 1
    print(i)
