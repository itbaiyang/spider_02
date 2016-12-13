#!/usr/bin/python

from pymongo import MongoClient

client = MongoClient()
db = client.spider_02
collection = db.job_51_u
position = collection.find().skip(1).limit(1)
i = 0
for item in position:
    i += 1
    for item_position in item["position"]:
        need = item_position['position_need']
        if need is None:
            print('none')
        elif '|' in need:
            need_arr = need.split('|')
            for item_arr in need_arr:
                if '年' in item_arr:
                    position['position_time'] = item_arr
                elif '人' in item_arr:
                    position['position_man'] = item_arr
                else:
                    position['position_p'] = item_arr
        else:
            if '年' in need:
                position_time = item_arr
            elif '人' in need:
                position_man = item_arr
            else:
                position_p = need

    if type(item["position"]) == str:
        # update = eval(item["position"])
        # collection.remove({"_id": item["_id"]})
        print("list")
        print(i)
    # try:
    #     update = eval(item["position"])
    #     # collection.update({"link": item["link"]}, {"$set": {"position": update}})
    # except:
    #     print("done")
    # i += 1
    # print(i)
