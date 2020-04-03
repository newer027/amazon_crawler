# -*- coding: utf-8 -*-
import pickle
from lxml.html import fromstring
from amazon.api import AmazonAPI
import requests
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


amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')
asin="B01LCDJ7LG"
product = amazon.lookup(ItemId=asin)
ean = product.ean
print(ean)


s = requests.Session()
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])


page = s.get('https://vendorexpress.amazon.com/supplyProductDetails?asin=B01LCDJ7LG&hasRetailOffer=false&externalIdType=EAN&externalId=0848061039948&isDfEligible=true&isPoEligible=true&productType=',headers=headers)
tree = fromstring(page.content)
print(tree.findtext('.//title'))
print(tree.xpath(".//*[@id='searchTerms']/@value"))


