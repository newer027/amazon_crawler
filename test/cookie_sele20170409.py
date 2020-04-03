# -*- coding: utf-8 -*-

import requests,datetime
from lxml.html import fromstring
from scrapy.selector import Selector
import os
from amazon.api import AmazonAPI
import pickle



agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Host': "www.amazon.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"
}

url_start='https://www.amazon.com/'
keyword='usb car charger'
s = requests.Session()
cookies = pickle.load(open(os.path.join(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0],'cookies_am.pkl'), "rb"))
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])
page = s.get(url_start+'s?field-keywords='+keyword+'&page=3',headers=headers)
tree = fromstring(page.content)
seller=(Selector(text=page.content).xpath(".//*[@id='result_3']/@data-asin")).extract()[0]
print(seller)

page = s.get(url_start+(Selector(text=page.content).xpath(".//*[@id='pagnNextLink']/@href")).extract()[0],headers=headers)
next=(Selector(text=page.content).xpath(".//*[@id='pagnNextLink']/@href")).extract()[0]
print(next)