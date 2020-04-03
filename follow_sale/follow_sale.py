# -*- coding: utf-8 -*-

import requests,datetime
from lxml.html import fromstring
from scrapy.selector import Selector
from .models import Product_seller,Product,Seller_change,Product_to_user
from celery import Celery
from django.contrib.auth import get_user_model
from asin_keyword.emails import send_email
import pytz,random
from django.utils import timezone
from core.amazon_api import get_url,amazon_api,country_url


def asin_title(asin,country):
    return get_url('gp/offer-listing/'+asin+'/ref=olp_page_5?ie=UTF8&startIndex=500',country=country)



def title_sql(asin,page,country):
    prod=Product.objects.filter(asin=asin,country=country)[0]
    try:
        amazon=amazon_api(country)
        product = amazon.lookup(ItemId=asin)
        prod.title=product.title
        prod.img_url=product.medium_image_url
        prod.detail_page_url=page.url
        prod.save()
    except:
        #print(page.status_code)
        tree = fromstring(page.content)
        title = tree.findtext('.//title')
        prod.title=title
        prod.detail_page_url=page.url
        prod.save()
    return prod


def title_sellers(page,product,country,initial):
    sell_items={}
    counter = 12
    not_first=False
    try:
        if Product_seller.objects.filter(product=product):
            not_first=True
    except:
        not_first=False
    while counter>0:
        counter -= 1
        for i in range(10):
            try:
                #//*[@id="olpOfferList"]/div/div/div[2]/div[3]/h3/span/a
                if Selector(text=page.content).xpath(".//*[@id='olpOfferList']/div/div/div["+str(i+2)+"]/div[4]/h3/span//a/@href"):
                    seller=(Selector(text=page.content).xpath(".//*[@id='olpOfferList']/div/div/div["+str(i+2)+"]/div[4]/h3/span//a/@href").extract()[0]).split("=")[-1]
                    sell_url=country_url(country)[:-1]+(Selector(text=page.content).xpath(".//*[@id='olpOfferList']/div/div/div["+str(i+2)+"]/div[4]/h3/span//a/@href").extract()[0])
                    name=fromstring(page.content).findtext('.//*[@id="olpOfferList"]/div/div/div['+str(i+2)+']/div[4]/h3/span/a')
                else:
                    seller=(Selector(text=page.content).xpath(".//*[@id='olpOfferList']/div/div/div["+str(i+2)+"]/div[3]/h3/span//a/@href").extract()[0]).split("=")[-1]
                    sell_url=country_url(country)[:-1]+(Selector(text=page.content).xpath(".//*[@id='olpOfferList']/div/div/div["+str(i+2)+"]/div[3]/h3/span//a/@href").extract()[0])
                    name=fromstring(page.content).findtext('.//*[@id="olpOfferList"]/div/div/div['+str(i+2)+']/div[3]/h3/span/a')


                price=fromstring(page.content).findtext('.//*[@id="olpOfferList"]/div/div/div['+str(i+2)+']/div[1]/span[1]').strip()
                sell_items[seller]={'seller':seller,'name':name,'price':price,'sell_url':sell_url}
                print(sell_items)

            except:
                print('寻找页面元素的逻辑错误')
                #product_seller.mark_time=datetime.datetime.now()

        if Selector(text=page.content).xpath("//ul[@class='a-pagination']//a/@href") != '#' and Selector(text=page.content).xpath("//ul[@class='a-pagination']//a/@href"):
            url_path = Selector(text=page.content).xpath("//ul[@class='a-pagination']//a/@href").extract()[0]
            page = get_url(url_path,country=country)


    if not sell_items:
        return "没有跟卖卖家"

    if initial:
        for seller_id in sell_items:
            product_seller=Product_seller(product=product,name=sell_items[seller_id]['name'],
                            seller_id=seller_id,price=sell_items[seller_id]['price'],sell_url=sell_items[seller_id]['sell_url'])
            product_seller.save()
    else:
        changed = False
        for seller_id in sell_items:
            if not Product_seller.objects.filter(product=product,seller_id=seller_id):
                product_seller=Product_seller(product=product,name=sell_items[seller_id]['name'],sell_url=sell_items[seller_id]['sell_url'],
                            seller_id=seller_id,price=sell_items[seller_id]['price'])
                product_seller.save()
                if not_first and not Seller_change.objects.filter(product=product,status='old',created__gte=timezone.now()-datetime.timedelta(days=1)):
                    seller_change=Seller_change(product=product,status='new',name=sell_items[seller_id]['name'],sell_url=sell_items[seller_id]['sell_url'],
                                seller_id=seller_id,price=sell_items[seller_id]['price'],created=datetime.datetime.now())
                    seller_change.save()
                    changed = True

        for seller_id in sell_items:
            if Product_seller.objects.filter(product=product,seller_id=seller_id):
                Product_seller.objects.filter(product=product,seller_id=seller_id).update(flag=True)

        if changed and not_first:
            product_to_user = Product_to_user.objects.filter(product=product)
            users = product_to_user.values_list('user', flat=True)
            User = get_user_model()
            users = User.objects.filter(id__in=users)
            seller_change = Seller_change.objects.filter(product=product, created__gte=timezone.now()-datetime.timedelta(minutes=3))
            sellers = seller_change.values_list('name', flat=True)

            for user in users:
                message = "\n".join([u'{0},您好.'.format(user.username), u'{0}有跟卖出现:'.format(product.title),u'跟卖商家:',
                    ','.join([seller for seller in sellers]),u'详情请见:','/'.join(['amz668.com/follow_sale',product.slug]),
                    u'直达亚马逊:{0}'.format(page.url)])
                send_email(user.email, message, '出现新的跟卖商品')

        for product_seller in Product_seller.objects.filter(product=product, flag=False):
            seller_change=Seller_change(product=product,status='old',name=product_seller.name,
                        seller_id=product_seller.seller_id,price=product_seller.price,created=datetime.datetime.now())
            seller_change.save()
        Product_seller.objects.filter(product=product, flag=False).delete()
        Product_seller.objects.filter(product=product).update(flag=False)


app = Celery()
app.config_from_object('django.conf:settings')

@app.task(bind=True,time_limit=200,acks_late=True,default_retry_delay=60,max_retries=30)
def initial_task(self,asin,country):
    try:
        page=asin_title(asin,country)
        product=title_sql(asin,page,country)
        title_sellers(page,product,country,initial=True)

    except Exception as e:
        dt = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=(random.random()*100+20))
        self.retry(eta=dt, exc=e, max_retries=5)


@app.task(bind=True,time_limit=200,acks_late=True,default_retry_delay=30,max_retries=3)
def mail_task(self,asin,country):
    try:
        page=asin_title(asin,country)
        if page:
            product=Product.objects.filter(asin=asin,country=country)[0]
            title_sellers(page,product,country,initial=False)

    except Exception as e:
        dt = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=(random.random()*100+20))
        self.retry(eta=dt, exc=e, max_retries=5)


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


if Product_seller.objects.filter(product=product,seller_id=seller):
    product_seller=Product_seller.objects.filter(product=product,seller_id=seller)[0]
    product_seller.flag=True
else:
    product_seller=Product_seller(product=product,name=name,seller_id=seller,price=price)
    if not initial:
        seller_change=Seller_change(product=product,name=name,seller_id=seller,price=price,status='new')
        seller_change.save()
    Product_seller.flag=True
    product_seller.save()

sellers=Product_seller.objects.filter(product=product,flag=False)
for seller in sellers:
    seller.status='old'
    seller_change=Seller_change(product=product,name=seller.name,seller_id=seller.seller_id,price=seller.price,status='old')
    seller_change.save()
sellers=Product_seller.objects.filter(product=product)
for seller in sellers:
    seller.flag=False
"""

