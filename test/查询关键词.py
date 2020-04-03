# -*- coding: utf-8 -*-

import os
from amazon.api import AmazonAPI
import pickle
from lxml.html import fromstring
import requests
from lxml import etree
try:
    import cookielib
except:
    import http.cookiejar as cookielib

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
    'Host': "vendorexpress.amazon.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Referer": "https://vendorexpress.amazon.com/ap/signin?clientContext=133-8session-id=136-0923773-8779837; session-id-time=2082787201l; ub175614-7829853&openid.return_to=https%3A%2F%2Fvendorexpress.amazon.com%2Fap-post-redirect&prevRID=M6PX5H0V21HFC6YP68AJ&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_smp_us&openid.mode=checkid_setup&siteState=clientContext%3D147-5723462-9724065%2CsourceUrl%3Dhttps%253A%252F%252Fvendorexpress.amazon.com%252Fhome%253Fref%253DVE_LANDING%2Csignature%3Dby0LO8lptc0jLkrXHDM1S8GAVO8j3D&marketPlaceId=ATVPDKIKX0DER&pageId=amzn_smp_us&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
    "Cookie": "",
    "Connection": "keep-alive"
}
amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')

asin = 'B01LCDJ7LG'
product = amazon.lookup(ItemId=asin)
# product = amazon.lookup(ItemId=asin)
ean = product.ean
title = product.title
print('ean:'+ean,'title'+title)


session = requests.Session()
URL = 'https://vendorexpress.amazon.com/supplyProductDetails?asin=' + asin + '&hasRetailOffer=false&externalIdType=EAN&externalId=' + ean + '&isDfEligible=true&isPoEligible=true&productType='
req = session.get(URL,headers=headers)
tree = fromstring(req.content)
# print (req.content)
# print(tree.findtext('.//title'))
keyword = tree.xpath(".//*[@id='searchTerms']/@value")
print(keyword)

# def asin_to_keyword(asin):
#     item = {}
#     product = amazon.lookup(ItemId=asin)
#     ean = product.ean
#     item['ean'] = ean
#     item['title'] = product.title
#     print(ean)
#
#     s = requests.Session()
#     cookies = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cookies.pkl'), "rb"))
#     for cookie in cookies:
#         s.cookies.set(cookie['name'], cookie['value'])
#
#     page = s.get('https://vendorexpress.amazon.com/supplyProductDetails?asin=' + asin + '&hasRetailOffer=false&externalIdType=EAN&externalId=' + ean + '&isDfEligible=true&isPoEligible=true&productType=',headers=headers)
#     print(page.request.headers)
#     tree = fromstring(page.content)
#     print(tree.findtext('.//title'))
#     keyword = tree.xpath(".//*[@id='searchTerms']/@value")
#     print(keyword)
#     item['keyword'] = keyword
#     return item