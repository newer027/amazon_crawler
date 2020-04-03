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
    "Cookie": 'session-id=136-0923773-8779837; session-id-time=2082758401l; ubid-main=133-8175614-7829853; csm-hit=AW5Z10CZAW83SQXFRWQQ+s-CYGCYKNS9ED1YTPR2X80|1491809244802; ve-generic-tag=VE_LANDING; session-token="r+/m8IkA8TmyLVK7bNPl6lDhJSUi5EDOyhRgxRiLDb8jQDW6VjwNCJy5NmUvaPjKdFMjzmLW62QXIBxiClN5SNTFg9ipOGh/lXX2day0qua0/rcZVtsaCVg1s0C/o8ovOOrO26dXd/7yTXtZcv5gTx0ebn/4fSyEgqA+wm3J0b3BJltG8L2uK1qe3Ev1+VWMqmzkQ3a4GwzV5/IKwuXZUyGkHAinwswAT6n/YmlrQL0="; x-main="d@E4Mm?8FPKfhuQLo4PVSk3xXywC2X596xIalBAOGMcHc4EcayGT44jHGNC8mnus"; at-main=Atza|IwEBIPLBccYgNw7TmWtqQOpCuZPOR7LXm9XdzLzwvIAohbAkMsFos6ZfPKpNYNOAVxypC7VXLw67TUdOv4V0ecL10KvphAggtZxNQeBcx9If0_GxdDnIe3PxuJwdV98od15rnbcG3U8wAorzQUTtVRmygguYecpm6u3xuOQeR_x7GVXg2-Qv4nd1TVejKE-YDm1vBnykipJ5OaACgS99vDBon7gvT_2boNdOSIq1IO_SOH8cfYE-7SdmUK2dAw4VBBZP0UyjneOyhbF7g_VOsmEf-7dF133Unp9kI22R32-rpeTGxbnEbbklu8VmAiWSJfNCFjuug0TOA9OK20E1oDrp0awcJkbHQfd175fFi8EVIPdQeDhgPBN2B_zL0iOhoaDC76kZlPdAJquiEkPiE-_nNOJL; sess-at-main="qmhTvQJteZLTZQ+Fl2r7uny3ZC5aIbXZYRZQmQ2Zxes="; aws-target-static-id=1491808254659-832419; aws-target-session-id=1491808254660-494030; aws-target-visitor-id=1491808254660-335301.24_4; aws-target-data=%7B%22support%22%3A%221%22%7D; s_fid=68AA943284474029-32F15274DD73E976; s_dslv=1491808460406; s_dslv_s=First%20Visit; s_depth=5; s_vn=1523344255231%26vn%3D1; s_invisit=true; s_nr=1491808460407-New; sc_channel=PS; sc_campaign=acquisition_CN; sc_publisher=baidu; sc_medium=brandzone; sc_content=pc; sc_detail=title; sc_segment=101; sc_category=pc; sc_matchtype=exact; sc_country=CN; s_campaign=PS%7Cacquisition_CN%7Cbaidu%7Cbrandzone%7Cpc%7Ctitle%7C101%7Cpc%7Cexact%7CCN; regStatus=pre-register; c_m=PSbzclk.baidu.comPaid%20Searchaws; s_cc=true; aws-mkto-trk=id%3A112-TZM-766%26token%3A_mch-aws.amazon.com-1491808256369-53846; aws_lang=cn',
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