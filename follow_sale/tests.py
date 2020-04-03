import requests
from lxml.html import fromstring
from scrapy.selector import Selector


agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Host': "www.amazon.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"
}
s = requests.Session()

def asin_to_follow_sale(asin):
    page = s.get('https://www.amazon.com/gp/offer-listing/'+asin+'/ref=olp_page_5?ie=UTF8&startIndex=200',headers=headers)
    print(page.text)
    tree = fromstring(page.content)
    print(tree.findtext('.//title'))
    while True:
        for i in range(10):
            try:
                seller=(Selector(text=page.content).xpath(".//*[@id='olpOfferList']/div/div/div["+str(i+2)+"]/div[4]/h3/span//a/@href").extract()[0]).split("=")[-1]
                print(tree.findtext('.//*[@id="olpOfferList"]/div/div/div['+str(i+2)+']/div[4]/h3/span/a'),"的价格是", \
                    tree.findtext('.//*[@id="olpOfferList"]/div/div/div['+str(i+2)+']/div[1]/span[1]'),seller)
            except:
                pass
        path = Selector(text=page.content).xpath("//ul[@class='a-pagination']//a/@href").extract()[0]
        if path=="#":
            break
        page = s.get('https://www.amazon.com'+path,headers=headers)
        tree = fromstring(page.content)

asin_to_follow_sale('B003BZD08U')


#https://www.amazon.com/gp/offer-listing/B003BZD08U/ref=olp_page_8?ie=UTF8&startIndex=70
#https://www.amazon.com/gp/offer-listing/B003BZD08U/ref=olp_page_5?ie=UTF8&startIndex=200