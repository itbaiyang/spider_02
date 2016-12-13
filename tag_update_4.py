#!/usr/bin/python

from pymongo import MongoClient

client = MongoClient()
db = client.spider_02
collection = db.job_update
position = collection.find({"company_tag": {"$exists": True}}).skip(800000).limit(200000)
i = 800000
for item in position:
    try:
        update = eval(item["company_tag"])
        collection.update({"company_name": item["company_name"]}, {"$set": {"company_tag": update}})
    except:
        print("done")
    print(i)
    i += 1
