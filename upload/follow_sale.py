import requests,datetime
from lxml.html import fromstring
from scrapy.selector import Selector
from .models import Product_seller,Product,Seller_change
from django.db.models import F
import datetime
from core.amazon_api import country_url


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
    url_start=country_url(country)
    page = s.get(url_start+'gp/offer-listing/'+asin+'/ref=olp_page_5?ie=UTF8&startIndex=500',headers=headers)
    return page


def title_sql(asin,page,):
    tree = fromstring(page.content)
    title = tree.findtext('.//title')
    product = Product(title=title,asin=asin)
    product.save()
    return product


def title_sellers(page,product,initial):
    tree = fromstring(page.content)
    print(tree.findtext('.//title'))
    while True:
        for i in range(10):
            try:
                seller=(Selector(text=page.content).xpath(".//*[@id='olpOfferList']/div/div/div["+str(i+2)+"]/div[4]/h3/span//a/@href").extract()[0]).split("=")[-1]
                name=fromstring(page.content).findtext('.//*[@id="olpOfferList"]/div/div/div['+str(i+2)+']/div[4]/h3/span/a')
                price=fromstring(page.content).findtext('.//*[@id="olpOfferList"]/div/div/div['+str(i+2)+']/div[1]/span[1]')
                if Product_seller.objects.filter(seller_id=seller):
                    product_seller=Product_seller.objects.filter(seller_id=seller)[0]
                    product_seller.status='same'
                    product_seller.flag=True

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
            except:
                pass
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
    if not initial:
        sellers=Product_seller.objects.filter(product=product).exclude(status='same')
    return sellers


def initial_task(asin,country):
    page=asin_title(asin,country)
    product=title_sql(asin,page)
    sellers=title_sellers(page,product,initial=True)
    return sellers


def mail_task(asin,country):
    page=asin_title(asin,country)
    product=Product.objects.filter(asin=asin)[0]
    title_sellers(page,product,initial=False)
    return product

"""
def asin_to_follow_sale(asin):
    page = s.get('https://www.amazon.com/gp/offer-listing/'+asin+'/ref=olp_page_5?ie=UTF8&startIndex=500',headers=headers)
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
"""

