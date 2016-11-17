
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('127.0.0.1', 27017)
client.spider.authenticate('baiyang', 'baiyang')
db = client.spider
collection = db.job51


def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    bid_sh = {}
    pass
    name = bs.find('h1').string
    detail = bs.find(class_='ltype')
    summary = bs.find(class_='con_msg')
    position = bs.find(class_='table_list')
    # con = content.find(class_='tHeader_mk')
    bid_sh['name'] = name
    bid_sh['detail'] = str(detail)
    bid_sh['summary'] = str(summary)
    if str(position) == 'None':
        collection.update({"link": link}, {"$set": {"name": name, "detail": str(detail), "summary": str(summary),
                                                    "company": ''}})
    else:
        list_ul = position.find(id='joblistdata')
        list_item = list_ul.find_all(class_='el')
        position_arr = []
        for item in list_item:
            position_detail = {}
            pass
            position_detail['position_name'] = item.find('a').string
            position_detail['position_need'] = item.find(class_='t2').string
            position_detail['position_addr'] = item.find(class_='t3').string
            position_detail['position_money'] = item.find(class_='t4').string
            position_detail['position_time'] = item.find(class_='t5').string
            position_arr.append(position_detail)
        bid_sh['position'] = str(position_arr)
    # collection.insert(bid_sh)
        collection.update({"link": link}, {"$set": {"name": name, "detail": str(detail), "summary": str(summary),
                                                    "position": str(position_arr), "company": ''}})
    # collection.update()
    print(bid_sh['name'])
    return final
if __name__ == '__main__':
    for i in collection:
        link = i['link']
        result = get_data(i['company'])
