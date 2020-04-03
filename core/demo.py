#/usr/bin/env python
import re,pytz,random,time,logging,csv,json
from lxml.html import fromstring
from scrapy.selector import Selector
from datetime import datetime,timedelta
from core.amazon_api import get_url
from celery import Celery
from django.utils import timezone
from io import StringIO
from django.conf import settings
from django.core.mail import EmailMessage
from hashlib import md5
from urllib.parse import quote
from http.client import HTTPConnection


logger = logging.getLogger(__name__)

DATE_FORMAT = '%m/%d/%Y'
FILENAME_DATE_FORMAT = '%Y_%m_%d'
TIME_FORMAT = '%I:%M %p'

app = Celery()
app.config_from_object('django.conf:settings')


appid = '20170802000070145'
secretKey = 'l0nqT09t2g0LmUATLs0l'
fromLang = 'en'
toLang = 'zh'
salt = random.randint(32768, 65536)
errors='strict'
encoding='utf-8'



def find_item(amazon,asin):
    item = {}
    product = amazon.lookup(ItemId=asin)
    item['title'] = product.title
    item['img_url'] = product.medium_image_url
    item['detail_page_url'] = product.detail_page_url
    item['brand'] = product.brand
    return item


class GlucoseCsvReport(object):

    def __init__(self, product):
        self.product=product
        self.user = product.user
        self.email_footer = '----------\nhttp://%s' % \
                            settings.SITE_DOMAIN

    def generate(self):
        data = Review_detail.objects.filter(product=self.product)
        csv_data = StringIO()
        try:
            headers = ['采集日期', '品牌', '星级', 'ASIN','买家ID','买家URL','评论日期','评论内容','中文翻译','是否优惠购买']

            writer = csv.writer(csv_data)
            writer.writerow(headers)

            for item in data:
                row = [
                    self.product.created.strftime(DATE_FORMAT),
                    self.product.brand,
                    item.star,
                    self.product.asin,
                    item.customer_id,
                    item.customer_url,
                    item.review_time,
                    item.review_text,
                    item.review_chinese,
                ]

                writer.writerow(row)

            logging.info('CSV report generated for %s', self.user)

            return csv_data.getvalue()

        finally:
            csv_data.close()

    def email(self, recipient, subject='', message=''):
        message = '%s\n\n\n%s' % (message, self.email_footer)

        email = EmailMessage(
            from_email=settings.DEFAULT_FROM_EMAIL,
            subject=subject,
            body=message,
            to=[recipient.email],
            headers={'Reply-To': self.user.email},
        )

        attachment_filename = '%s %s Reviews %s.csv' % (self.product.country,self.product.asin,time.strftime(FILENAME_DATE_FORMAT,time.gmtime()))

        email.attach(attachment_filename, self.generate(), 'text/csv')
        email.send()


def translate(q):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    sign = appid+q+str(salt)+secretKey
    m1 = md5()
    m1.update(str(sign).encode(encoding, errors))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    count=0
    while count<4:
        try:
            httpClient = HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            #response是HTTPResponse对象
            response = httpClient.getresponse()
            string = response.read().decode('utf-8')
            if string:
                if httpClient:
                    httpClient.close()
                json_obj = json.loads(string)
                return json_obj['trans_result'][0]['dst']
        except:
            time.sleep(0.1+random.random()*0.2)
            continue
        finally:
            if httpClient:
                httpClient.close()
    return None

