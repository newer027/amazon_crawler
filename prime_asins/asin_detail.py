# -*- coding: utf-8 -*-


from core.amazon_api import amazon_api
from prime_asins.models import Asin_detail
from celery import Celery
import pytz,datetime,time,random
from amazon.api import AsinNotFound
try:
    import cookielib
except:
    import http.cookiejar as cookielib


app = Celery()
app.config_from_object('django.conf:settings')

@app.task(bind=True,time_limit=200,acks_late=True)
def asin_to_detail(self,fu_asin,country):
    asin_detail=Asin_detail.objects.filter(fu_asin=fu_asin,country=country)[0]
    try:

        count=0
        while count<5:
            try:
                count+=1
                amazon = amazon_api(country)
                product=amazon.lookup(ItemId=fu_asin)
            except AsinNotFound:
                asin_detail.img_url=u'http://www.amz668.com/static/images/icons/icon.jpg'
                asin_detail.save()
                return '没有找到ASIN'
            except:
                time.sleep(0.1+random.random()*0.15)
                continue

        asin_detail.label=product.label
        asin_detail.brand=product.brand
        if product.large_image_url:
            asin_detail.img_url=product.large_image_url
        else:
            try:
                if product.images[0].LargeImage:
                    asin_detail.img_url=product.images[0].LargeImage.URL
                else:
                    asin_detail.img_url=u'http://www.amz668.com/static/images/icons/icon.jpg'
            except:
                asin_detail.img_url=u'http://www.amz668.com/static/images/icons/icon.jpg'
        asin_detail.detail_page_url=product.detail_page_url
        asin_detail.price=product.formatted_price
        asin_detail.bsr_rank=product.sales_rank
        asin_detail.save()
        return fu_asin
    except Exception as e:
        dt = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=4)
        self.retry(eta=dt, exc=e, max_retries=1)

