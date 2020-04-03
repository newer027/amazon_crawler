# -*- coding: utf-8 -*-

import requests,datetime
from lxml.html import fromstring
from scrapy.selector import Selector
import datetime
from core.amazon_api import country_url
from follow_sale.models import Product,Product_seller,Seller_change

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

def asin_title(asin,country):
    headers['Host']=country_url(country).split("/")[2]
    url_start=country_url(country)
    page = s.get(url_start+'gp/offer-listing/'+asin+'/ref=olp_page_5?ie=UTF8&startIndex=500',headers=headers)
    return page


def title_sql(asin,page,country):
    print(page.status_code)
    tree = fromstring(page.content)
    title = tree.findtext('.//title')
    print(title)
    product = Product(title=title,asin=asin,country=country)
    product.save()
    return product


def title_sellers(page,product,initial):
    tree = fromstring(page.content)
    print(tree.findtext('.//title'))
    while True:
        for i in range(10):
            try:
                #//*[@id="olpOfferList"]/div/div/div[2]/div[3]/h3/span/a

                seller=(Selector(text=page.content).xpath(".//*[@id='olpOfferList']/div/div/div["+str(i+2)+"]/div[3]/h3/span//a/@href").extract()[0]).split("=")[-1]
                name=fromstring(page.content).findtext('.//*[@id="olpOfferList"]/div/div/div['+str(i+2)+']/div[3]/h3/span/a')

                price=fromstring(page.content).findtext('.//*[@id="olpOfferList"]/div/div/div['+str(i+2)+']/div[1]/span[1]')
                print(seller,name,price)
                if Product_seller.objects.filter(seller_id=seller):
                    product_seller=Product_seller.objects.filter(seller_id=seller)[0]
                    product_seller.status='same'
                    product_seller.flag=True
            except:
                print('寻找页面元素的逻辑错误')

                #product_seller.mark_time=datetime.datetime.now()

            else:
                product_seller=Product_seller(product=product,name=name,seller_id=seller,price=price)
                if initial:
                    product_seller.status='same'
                else:
                    seller_change=Seller_change(product=product,name=name,seller_id=seller,price=price,status='new')
                    seller_change.save()
                Product_seller.flag=True
                product_seller.save()
        url_path=None
        try:
            url_path = Selector(text=page.content).xpath("//ul[@class='a-pagination']//a/@href").extract()[0]
        except:
            pass
        if url_path=="#" or url_path==None:
            break
        page = s.get('https://www.amazon.com'+url_path,headers=headers)
        print(url_path)

    sellers=Product_seller.objects.filter(product=product,flag=False)
    for seller in sellers:
        seller.status='old'
        seller_change=Seller_change(product=product,name=seller.name,seller_id=seller.seller_id,price=seller.price,status='old')
        seller_change.save()
    sellers=Product_seller.objects.filter(product=product)
    for seller in sellers:
        seller.flag=False

def test():
    page=asin_title('B00HZVQ8DA','de')
    product=title_sql('B00HZVQ8DA',page,'de')
    title_sellers(page,product,initial=True)


def rank_in_web(asin,keyword,node,country):
    info = {'rank':None,'page':None}
    if country=='us':
        url_start='https://www.amazon.com/s?field-keywords='
        try:
            page = s.get(url_start+keyword+'&node='+node+'&page=1',headers=headers)
            item_amount=int((Selector(text=page.content).xpath('.//*[@id="s-result-count"]/text()').extract()[0])[2:4])
            tree = fromstring(page.content)
            print(tree.findtext('.//title'))
            print(int(item_amount)-24)

            for j in range(24):
                try:
                    seller=(Selector(text=page.content).xpath(".//*[@id='result_"+str(24*i+j+1)+"']/div/div/div/div[2]/div[1]/div[1]//a/@href").extract()[0]).split("/")[5]
                    print(seller)
                    #if seller==asin:
                    #    info = {'rank':j+1,'page':i+1}
                    #    print("在类别",node,"下搜索关键词",keyword,":",asin,"排名第",i+1,"页,第",j+1,"名")
                    #    return info
                except:
                    return info

        except:
            return info


    """
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
    """
#rank_in_web('B01NA9UG56','juicer','172282',country='us')



"""
('ArtsAndCrafts','2617941011'),
('Automotive','15684181'),('Baby','165796011'),('Beauty','3760911'),
('Books','283155'),('Electronics','172282'),
('GiftCards','GiftCards'),('Grocery','16310211')
('HealthPersonalCare','3760901'),
('Industrial','16310161'),('Magazines','599858'),('MobileApps','MobileApps'),('Movies','2625373011'),
('MP3Downloads','2334092011'),('Music','5174'),('MusicalInstruments','11091801'),
('OfficeProducts','1064954'),('PetSupplies','2619533011'),
('Software','229534'),('SportingGoods','3375251'),('Tools','165793011'),('Toys','165793011'),('All','')

https://www.amazon.com/s?field-keywords=juicer&node=599872&page=1
"""