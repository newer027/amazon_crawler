# -*- coding: utf-8 -*-
from review_qa_collect.models import Product, QA_detail, Review_detail
from core.amazon_api import get_url,country_url
import pytz,random,time,re
from lxml.html import fromstring
from scrapy.selector import Selector
from datetime import datetime,timedelta
from celery import Celery

import csv
from io import StringIO
import logging
from django.conf import settings
from django.core.mail import EmailMessage


logger = logging.getLogger(__name__)

DATE_FORMAT = '%m/%d/%Y'
FILENAME_DATE_FORMAT = '%Y_%m_%d'
TIME_FORMAT = '%I:%M %p'

app = Celery()
app.config_from_object('django.conf:settings')


@app.task(bind=True,time_limit=500,acks_late=True,default_retry_delay=3, max_retries=3)
def qa_collect(self,asin,country='us'):
    try:
        product=Product.objects.filter(asin=asin,country=country)[0]
        page=get_url('ask/questions/asin/'+asin+'/ref=ask_ql_psf_ql_hza?sort=SUBMIT_DATE', country)
        tree = fromstring(page.content)
        print(tree.findtext('.//title'))
        if tree.findtext('.//title')=='Robot Check' or tree.findtext('.//title')=='Amazon CAPTCHA':
            info = {'to':0}
            return info

        if Selector(text=page.content).xpath('.//*[@id="noResultsTitle"]'):
            info = {'to':0}
            return info

        qa_collection={}
        if Selector(text=page.content).xpath("//ul[@class='a-pagination']/li[@class='a-last']//a/@href"):
            page_num=0
            while True:
                boxes=Selector(text=page.content).xpath(".//*[@class='a-section askTeaserQuestions']/div[@class='a-fixed-left-grid a-spacing-base']")
                for box in boxes:
                    answer_url,answer,answer_user,qa_time=None,None,None,None
                    vote=int(box.xpath(".//ul[@class='vote voteAjax']/li[2]/span[1]/text()").extract()[0])
                    question=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-small']//a[@class='a-link-normal']/text()").extract()[0]
                    try:
                        qa_time=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-fixed-left-grid-col a-col-right']/span[2]/text()").extract()[-1:][0]
                    except:
                        pass
                    try:
                        if box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-fixed-left-grid-col a-col-right']/span[1]/text()").extract() and country != 'jp':
                            answer=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-fixed-left-grid-col a-col-right']/span[1]/text()").extract()[0]
                        elif box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-fixed-left-grid-col a-col-right']/span[1]/text()").extract() and country == 'jp':
                            answer=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-fixed-left-grid-col a-col-right']/span[1]/text()").extract()[0]
                            if answer == "":
                                try:
                                    answer=" ".join(box.xpath(".//span[@class='askLongText']/text()").extract()).strip()
                                except:
                                    pass
                        else:
                            answer=" ".join(box.xpath(".//span[@class='askLongText']/text()").extract()).strip()
                    except:
                        pass
                    try:
                        answer_user=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-fixed-left-grid-col a-col-right']/span[2]/text()").extract()[0]
                    except:
                        pass
                    try:
                        answer_quan=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-section a-spacing-none a-spacing-top-mini']/a/text()").extract()[0]
                        answer_quan = re.search(r'\d+', answer_quan).group(0)
                    except:
                        pass
                    try:
                        answer_url=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-section a-spacing-none a-spacing-top-mini']/a/@href").extract()[0]
                        answer_url=country_url(country)[:-1]+answer_url
                        #print("answer_url:",answer_url)
                    except:
                        pass

                    #print(answer_user,qa_time)
                    if answer_user == None:
                        pass
                    elif answer_user==qa_time:
                        if country in['us','uk','ca','de']:
                            name_date=re.split(' on |By |Von | am ', answer_user)
                        elif country=='it':
                            name_date=re.split(' in |Da ', answer_user)
                        elif country=='fr':
                            name_date=re.split(' le |Par ', answer_user)
                        elif country=='es':
                            name_date=re.split(' el |Por ', answer_user)
                        elif country=='jp':
                            name_date=re.split('投稿者: |、投稿日: ', answer_user)
                        answer_user=name_date[1]
                        qa_time=name_date[2]
                    else:
                        answer_user=re.split(' on |By |Von | am ', answer_user)[-1:][0]
                        qa_time=re.split(' on |By |Von | am ', qa_time)[-1:][0]

                    if answer_url and answer_quan:
                        qa_collection[question]={'vote':vote,'question':question,'qa_time':qa_time.strip(),'answer':answer,'answer_user':answer_user.strip(),'answer_quan':answer_quan,'answer_url':answer_url}
                    elif answer:
                        qa_collection[question]={'vote':vote,'question':question,'qa_time':qa_time.strip(),'answer':answer,'answer_user':answer_user.strip()}
                print(len(qa_collection))

                if Selector(text=page.content).xpath("//ul[@class='a-pagination']/li[@class='a-last']//a/@href") and page_num<200:
                    time.sleep(2+random.random()*5)
                    page=get_url((Selector(text=page.content).xpath("//ul[@class='a-pagination']/li[@class='a-last']//a/@href")).extract()[0],country=country)
                    page_num += 1
                else:
                    break

        else:
            boxes=Selector(text=page.content).xpath(".//*[@class='a-section askTeaserQuestions']/div[@class='a-fixed-left-grid a-spacing-base']")
            for box in boxes:
                answer_url,answer,answer_user,qa_time=None,None,None,None
                vote=int(box.xpath(".//ul[@class='vote voteAjax']/li[2]/span[1]/text()").extract()[0])
                question=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-small']//a[@class='a-link-normal']/text()").extract()[0]
                try:
                    qa_time=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-fixed-left-grid-col a-col-right']/span[2]/text()").extract()[-1:][0]
                except:
                    pass
                try:
                    if box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-fixed-left-grid-col a-col-right']/span[1]/text()").extract():
                        answer=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-fixed-left-grid-col a-col-right']/span[1]/text()").extract()[0]
                    else:
                        answer=" ".join(box.xpath(".//span[@class='askLongText']/text()").extract()).strip()
                except:
                    pass
                try:
                    answer_user=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-fixed-left-grid-col a-col-right']/span[2]/text()").extract()[0]
                except:
                    pass
                try:
                    answer_quan=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-section a-spacing-none a-spacing-top-mini']/a/text()").extract()[0]
                    answer_quan = re.search(r'\d+', answer_quan).group(0)
                except:
                    pass
                try:
                    answer_url=box.xpath(".//div[@class='a-fixed-left-grid a-spacing-base']//div[@class='a-section a-spacing-none a-spacing-top-mini']/a/@href").extract()[0]
                    answer_url=country_url(country)[:-1]+answer_url
                except:
                    pass

                if answer_user == None:
                    pass
                elif answer_user==qa_time:
                    if country in['us','uk','ca','de']:
                        name_date=re.split(' on |By |Von | am ', answer_user)
                    elif country=='it':
                        name_date=re.split(' in |Da ', answer_user)
                    elif country=='fr':
                        name_date=re.split(' le |Par ', answer_user)
                    elif country=='es':
                        name_date=re.split(' el |Por ', answer_user)
                    elif country=='jp':
                        name_date=re.split('投稿者: |、投稿日: ', answer_user)
                    answer_user=name_date[1]
                    qa_time=name_date[2]
                else:
                    answer_user=re.split(' on |By |Von | am ', answer_user)[-1:][0]
                    qa_time=re.split(' on |By |Von | am ', qa_time)[-1:][0]

                if answer_url and answer_quan:
                    qa_collection[question]={'vote':vote,'question':question,'qa_time':qa_time,'answer':answer,'answer_user':answer_user,'answer_quan':answer_quan,'answer_url':answer_url}
                elif answer:
                    qa_collection[question]={'vote':vote,'question':question,'qa_time':qa_time,'answer':answer,'answer_user':answer_user}

        for qa in qa_collection:
            try:
                num=qa_collection[qa]['answer_quan']
            except:
                num="1"
            try:
            #if qa_collection[qa]['answer_url']:
                QA_detail.objects.get_or_create(product=product,vote=qa_collection[qa]['vote'],question=qa_collection[qa]['question'],qa_time=qa_collection[qa]['qa_time'],
                    answer=qa_collection[qa]['answer'],answer_person=qa_collection[qa]['answer_user'],num=num,answer_url=qa_collection[qa]['answer_url'])
            except:
                QA_detail.objects.get_or_create(product=product,vote=qa_collection[qa]['vote'],question=qa_collection[qa]['question'],qa_time=qa_collection[qa]['qa_time'],
                    answer=qa_collection[qa]['answer'],answer_person=qa_collection[qa]['answer_user'],num=num)
            #except:
            #    pass

        #report = GlucoseCsvReport(product)
        #report.email(product.user, 'subject', 'message')

    except Exception as e:
        dt = datetime.now(pytz.utc) + timedelta(seconds=40)
        self.retry(eta=dt, exc=e, max_retries=2)


def find_item(amazon,asin):
    item = {}
    product = amazon.lookup(ItemId=asin,)
    item['title'] = product.title
    item['img_url'] = product.medium_image_url
    item['detail_page_url'] = product.detail_page_url
    return item


class GlucoseCsvReport(object):

    def __init__(self, product):
        self.product=product
        self.user = product.user
        self.email_footer = '----------\nhttp://%s' % \
                            settings.SITE_DOMAIN

    def generate(self):
        data = QA_detail.objects.filter(product=self.product)
        csv_data = StringIO()
        try:
            headers = ['回答日期', '问题', '答案', '回答人','VOTE数量','答案总数','所有答案链接']

            writer = csv.writer(csv_data)
            writer.writerow(headers)

            for item in data:
                row = [
                    item.answer_time,
                    item.question,
                    item.answer,
                    item.answer_person,
                    item.num,
                    item.answer_url,
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

        attachment_filename = '%s %s Question_Answer %s.csv' % (self.product.country,self.product.asin,time.strftime(FILENAME_DATE_FORMAT,time.gmtime()))

        email.attach(attachment_filename, self.generate(), 'text/csv')
        email.send()


def get_name_date(text):
    pattern='on'
    for match in re.finditer(pattern,text):
        s = match.start()
        e = match.end()
        name = text[5:s-1]
        date = text[e+1:]
        return {"name":name,"date":date}
