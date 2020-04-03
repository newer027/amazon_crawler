# -*- coding: utf-8 -*-
from review_qa_collect.models import Product, QA_detail, Review_detail
from core.amazon_api import get_url
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
toLang = 'zh'
salt = random.randint(32768, 65536)
errors='strict'
encoding='utf-8'

@app.task(bind=True,time_limit=60*30,acks_late=True,default_retry_delay=3, max_retries=3)
def review_collect(self,asin,country='us'):
    try:
        product=Product.objects.filter(asin=asin,country=country)[0]
        page=get_url('product-reviews/'+asin+'/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent&pageNumber=1&reviewerType=all_reviews',country)
        tree = fromstring(page.content)
        print(tree.findtext('.//title'))
        if tree.findtext('.//title')=='Robot Check' or tree.findtext('.//title')=='Amazon CAPTCHA':
            info = {'to':0}
            return info

        if Selector(text=page.content).xpath('.//*[@id="noResultsTitle"]'):
            product.review_qa_complete_time=timezone.now()
            product.save()
            info = {'to':0}
            return info

        review_monitors={}
        if country in ['de','uk','fr','it','es']:
            star=(Selector(text=page.content).xpath('.//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/text()').extract()[0]).split(" ")[0]
        elif country=='jp':
            star=(Selector(text=page.content).xpath('.//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/text()').extract()[0])[-3:]
        else:
            star=(Selector(text=page.content).xpath('.//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/a/span/text()').extract()[0]).split(" ")[0]
        reviews_quant=Selector(text=page.content).xpath('.//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span/text()').extract()[0]
        reviews_quant=int(re.sub(",","",reviews_quant))
        product.reviews_url=page.url
        product.star=star
        product.reviews_quant=reviews_quant
        product.save()
        print(reviews_quant)

        page_num=0
        if reviews_quant>10:
            while True:
                try:
                    for i in range(10):
                        star=int(Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[1]/a[1]/@title").extract()[i][0:1])
                        customer_id=(Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[2]/span//a/@href").extract()[i]).split("/")[4]
                        review_text=(Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[4]/span/text()").extract()[i])
                        review_time=Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[2]/span[4]/text()").extract()[i]
                        if country != 'jp':
                            review_time=review_time[3:]
                        normal=Selector(text=page.content).xpath(".//*[@class='a-section review']/div").extract()[0]
                        regex=re.compile('reviews:filter-action:push-state')
                        #eview_chinese=translate(review_text)
                        if regex.search(normal):
                            normal=True
                        else:
                            normal=False
                        review_monitors[customer_id]={'star':star,'customer_id':customer_id,'review_time':review_time,'review_text':review_text,'normal':normal}
                        #review_monitors[customer_id]={'star':star,'customer_id':customer_id,'review_time':review_time,'review_text':review_text,'review_chinese':review_chinese,'normal':normal}
                    print(page_num,len(review_monitors))
                except:
                    pass
                if Selector(text=page.content).xpath("//ul[@class='a-pagination']/li[@class='a-last']//a/@href") and page_num<200:
                    time.sleep(0.2+random.random()*0.5)
                    page=get_url((Selector(text=page.content).xpath("//ul[@class='a-pagination']/li[@class='a-last']//a/@href")).extract()[0],country=country)
                    page_num += 1
                else:
                    break

        else:
            try:
                for i in range(10):
                    star=int(Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[1]/a[1]/@title").extract()[i][0:1])
                    customer_id=(Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[2]/span//a/@href").extract()[i]).split("/")[4]
                    review_text=(Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[4]/span/text()").extract()[i])
                    review_time=Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[2]/span[4]/text()").extract()[i]
                    if country != 'jp':
                        review_time=review_time[3:]
                    normal=Selector(text=page.content).xpath(".//*[@class='a-section review']/div").extract()[i]
                    #review_chinese=translate(review_text)
                    regex=re.compile('reviews:filter-action:push-state')
                    if regex.search(normal):
                        normal=True
                    else:
                        normal=False
                    review_monitors[customer_id]={'star':star,'customer_id':customer_id,'review_time':review_time,'review_text':review_text,'normal':normal}
                    #review_monitors[customer_id]={'star':star,'customer_id':customer_id,'review_time':review_time,'review_text':review_text,'review_chinese':review_chinese,'normal':normal}
                print("length of reviews:",len(review_monitors))
            except:
                pass

        product.review_qa_complete_time=timezone.now()
        product.save()
        for customer_id in review_monitors:
            #,review_chinese=review_monitors[customer_id]['review_chinese']
            Review_detail.objects.get_or_create(product=product,star=review_monitors[customer_id]['star'],customer_id=customer_id,
                                        review_time=review_monitors[customer_id]['review_time'],review_text=review_monitors[customer_id]['review_text'],
                                        normal=review_monitors[customer_id]['normal'])
        info = {'to':page_num}
        return info

        #report = GlucoseCsvReport(product)
        #report.email(product.user, 'subject', 'message')

    except Exception as e:
        dt = datetime.now(pytz.utc) + timedelta(seconds=40)
        self.retry(eta=dt, exc=e, max_retries=2)


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


def translate(q,fromLang = 'en'):
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
            response = httpClient.getresponse()
            string = response.read().decode('utf-8')
            if string:
                if httpClient:
                    httpClient.close()
                json_obj = json.loads(string)
                time.sleep(0.4)
                return json_obj['trans_result'][0]['dst']
        except:
            time.sleep(0.1+random.random()*0.2)
            continue
        finally:
            if httpClient:
                httpClient.close()
    return None
