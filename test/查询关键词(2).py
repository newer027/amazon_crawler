# -*- coding: utf-8 -*-

from amazon.api import AmazonAPI
from lxml.html import fromstring
import requests

repeat_time = 0
while repeat_time < 1:
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
        'Host': "vendorexpress.amazon.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Referer": "https://vendorexpress.amazon.com/ap/signin?clientContext=133-8session-id=136-0923773-8779837; session-id-time=2082787201l; ub175614-7829853&openid.return_to=https%3A%2F%2Fvendorexpress.amazon.com%2Fap-post-redirect&prevRID=M6PX5H0V21HFC6YP68AJ&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_smp_us&openid.mode=checkid_setup&siteState=clientContext%3D147-5723462-9724065%2CsourceUrl%3Dhttps%253A%252F%252Fvendorexpress.amazon.com%252Fhome%253Fref%253DVE_LANDING%2Csignature%3Dby0LO8lptc0jLkrXHDM1S8GAVO8j3D&marketPlaceId=ATVPDKIKX0DER&pageId=amzn_smp_us&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
        "Cookie": 'session-id=140-9796142-4857756; session-id-time=2082787201l; ubid-main=133-8175614-7829853; csm-hit=YV9BAN4660FVX0NHNA7B+s-F6WVS0A9787CYGSYFKKC|1491826238147; ve-generic-tag=VE_LANDING; aws-target-static-id=1491808254659-832419; aws-target-visitor-id=1491808254660-335301.24_4; aws-target-data=%7B%22support%22%3A%221%22%7D; s_fid=68AA943284474029-32F15274DD73E976; s_dslv=1491820538504; s_vn=1523344255231%26vn%3D3; s_nr=1491820538505-Repeat; regStatus=pre-register; a-ogbcbff=1; lc-main=en_US; x-wl-uid=1Y68mqjXari7EbuT0evsva36pLGKnXfHRa6tIc2ajJHT1NgdnoFqfV+4Humtud1jDnAw2WTQKwij8+gouK3yXTw==; session-token="ccCpwot/ZWMylb1DmlxVCFi3IrJpw2LVvkJvFsp/L5cFTSI9zmQ5yug2yGsTnV/rUQxPzANHzw+L9a1dvTd8qLnqVxLkvZle4QB11DWGczwYCTu8QxvEb9sp/GUm46MWweaNtbiClHKH/hqsmxGUwbM9P/vNdMQVwCYE3M3OWx1cOR9E4rXy/4fPwmsvjdg+z/ZDZrJuX62AO1EDhC0O1lwoHxfUiAu0VCNMUoonuNA="; x-main="O3BZO4Tx74NJFn4vtdjFfQfiuP5KGGu8jAGOcewcMAEmAPVVhGIDBrU?fI1qrtSt"; at-main=Atza|IwEBIP-IO_J5ZKHJKKTOflZVOPsrninPQdGqQMsI3L3jw8Z8YKfPHdpPOnvG07coSJzq0bbIY69mA6nrYlDcQPwkZI-IVNW_WlGIlEEwfXIO6uVptZCpHCupMmMpHYPBeRW46r_HUuzzx0woOh0yi3vPbT0Ly0MEoCZn9lnDm4MbK9qCYobn89C8CFfHIVQ3jTU7epNPXyUob9GAuD3ncTOkMTJ_lCloQ7psH9CckPhXvE-nM4GU8088Sbk4-7wraE4yTy2vj595PwEDebMmtOep-Rk_EmHjOuo_HX8Fb8iv1vMmj1WtP23ri5jZ2tsjnzB-UvR9D67Bpxn8DBIE_l2sqOwYdQQoGxAitKy9oWNRbQ6LXsVwRjbKny6ZoqgngjQZGG2P-ICvIHg3g1KLma3Mc0ik; sess-at-main="4juCypssTzn3YrRQPr/COtwvPAvKTmlzovckR80bwVM="'
        ,"Connection": "keep-alive"
    }
    amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')

    asin = 'B01MZXSHOX'
    product = amazon.lookup(ItemId=asin)
    ean = product.ean
    print (ean)
    upc = product.upc
    print (upc)
    title = product.title
    print (title)

    session = requests.Session()
    URL = 'https://vendorexpress.amazon.com/supplyProductDetails?asin=' + asin + '&hasRetailOffer=false&externalIdType=EAN&externalId=' + ean + '&isDfEligible=true&isPoEligible=true&productType='
    req = session.get(URL,headers=headers)
    tree = fromstring(req.content)
    keyword = tree.xpath(".//*[@id='searchTerms']/@value")
    for item in keyword:
        print(item)

    repeat_time = repeat_time+1
    print repeat_time