#!/usr/bin/python

import requests
import random
import time
import socket
import re
import http.client
from pymongo import MongoClient
from bs4 import BeautifulSoup
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
client = MongoClient('127.0.0.1', 27017)
db = client.spider_02
collection = db.yingcai_job
# collection_company = db.company_china_yc


def get_content(url_list, data = None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url_list, headers=header, timeout=timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))
        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))
    return rep.text


def get_data(html_text):
    final = {}
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    data = bs.find(class_='base-company')
    treat_company = bs.find(class_='treat-company')
    job_data = bs.find(id="s_exampleJob")
    if data == None:
        print('no data')
    elif job_data == None:
        print('no job')
    else:
        if treat_company == None:
            print("no tags")
        else:
            company_tag_list = treat_company.find_all("li")
            tag_arr_zong = []
            for tag_list in company_tag_list:
                tag_item = tag_list.get_text()
                tag_arr_zong.append(tag_item)
            final['tag'] = tag_arr_zong
        company_name = data.find(class_='wrap-til').find('h1').string
        final['company_name'] = company_name
        company_item = job_data.find_all(class_="exj-child")
        job_arr = []
        for item in company_item:
            job = {}
            pass
            job['link'] = item.find("a").get('href')
            job['title'] = item.find("a").get_text()
            job['salary'] = item.find(class_="exj-e2").get_text()
            job_position = item.find(class_="exj-e3").get_text().strip()
            print(job_position)
            try:
                job['position'] = re.match(r'\[(.*?)\]', job_position).groups()[0]
            except:
                print("no position")
            job['time'] = item.find(class_="exj-e4").get_text()
            html_detail = get_content(job['link'])
            bs_detail = BeautifulSoup(html_detail, "html.parser")
            data_detail = bs_detail.find(class_='job_profile')
            job['job_intro_info'] = str(bs_detail.find(class_='job_intro_info'))
            job['job_intro_tag'] = str(bs_detail.find(class_='job_intro_tag'))
            data_temp = data_detail.find(class_='job_exp')
            if data_temp == None:
                print('no need')
            else:
                job['date'] = data_temp.get_text()
            company_tag = data_detail.find(class_='job_fit_tags')

            if company_tag == None:
                print('no tag')
            else:
                company_tag_li = company_tag.find_all("li")
                tag_arr = []
                for tag_list in company_tag_li:
                    tag_item = tag_list.get_text()
                    tag_arr.append(tag_item)
                job['tag'] = tag_arr
                job_arr.append(job)
        final['job'] = job_arr
        collection.insert(final)
    return final


if __name__ == '__main__':
    for i in range(400589, 500000):
        print(str(i))
        url = 'http://www.chinahr.com/company/20-'+str(i)+'.html'
    # url = 'http://www.chinahr.com/company/20-662922.html'
        html = get_content(url)
        result = get_data(html)

