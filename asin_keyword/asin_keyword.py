# -*- coding: utf-8 -*-

from core.amazon_api import amazon_api
import pickle,time,os,requests,random
from lxml.html import fromstring
from amazon.api import AsinNotFound
try:
    import cookielib
except:
    import http.cookiejar as cookielib


agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Host': "vendorexpress.amazon.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"
}


def asin_to_keyword(asin,country):
    item = {}

    count=0
    while count<5:
        try:
            count+=1
            amazon = amazon_api(country)
            product=amazon.lookup(ItemId=asin)
        except AsinNotFound:
            return item
        except:
            time.sleep(0.1+random.random()*0.15)
            continue

    else:
        item['ean'] = product.ean
        item['upc'] = product.upc
        item['img'] = product.medium_image_url
        item['url'] = product.detail_page_url
        item['title'] = product.title
        if not item['ean']:
            item['keyword'] = "因亚马逊后台问题，无法查询Search Terms"
            return item
        else:
            return get_ST(asin,item['ean'],item,country)


def get_ST(asin,ean,item,country):
    start='https://vendorexpress.amazon.eu/'
    if country=='us' or country=='ca':
        cookie='cookies_am.pkl'
        start='https://vendorexpress.amazon.com/'
    elif country=='jp':
        cookie='cookies_jp.pkl'
        start='https://vendorexpress.amazon.co.jp/'
    elif country=='uk':
        cookie='cookies_uk.pkl'
    elif country=='de':
        cookie='cookies_de.pkl'
    elif country=='fr':
        cookie='cookies_fr.pkl'
    elif country=='it':
        cookie='cookies_it.pkl'
    else:
        cookie='cookies_es.pkl'

    print(item,ean)
    s = requests.Session()
    cookies = pickle.load(open(os.path.join(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0],cookie), "rb"))
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    if country=='us':
        proxy={"http":"http://210.35.171.5:80"}
        page = s.get(start+'supplyProductDetails?asin=' + asin + '&hasRetailOffer=false&externalIdType=EAN&externalId=' + ean + '&isDfEligible=true&isPoEligible=true&productType=',proxies=proxy,headers=headers)
    else:
        page = s.get(start+'supplyProductDetails?asin=' + asin + '&hasRetailOffer=false&externalIdType=EAN&externalId=' + ean + '&isDfEligible=true&isPoEligible=true&productType=',headers=headers)
    print(page.status_code)
    tree = fromstring(page.content)
    print(tree.findtext('.//title'))
    keyword = tree.xpath(".//*[@id='searchTerms']/@value")
    if not keyword:
        item['keyword'] = "买家没有设定Search Terms"
    else:
        item['keyword'] = keyword[0]
    return item
