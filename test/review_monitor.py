# //*[@class="a-section review"]
# https://www.amazon.co.jp/product-reviews/B01KJR7772/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent&pageNumber=1
# //*[@class="a-section review"]/div[1]/a[1]/i/span
# //*[@class="a-section review"]/div[2]/span[1]//a/@href
# //*[@class="a-section review"]/div[2]/span[4]


import requests,datetime,pytz
from lxml.html import fromstring
from scrapy.selector import Selector
from .models import Rank,Keyword_rank
from core.amazon_api import country_url, pro_chi
from celery import Celery


agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Host': "www.amazon.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"
}


app = Celery()
app.config_from_object('django.conf:settings')


#@app.task(bind=True,time_limit=500,acks_late=True,default_retry_delay=3, max_retries=3)
def review_monitor(self,asin,country='us'):
    try:
        proxy=pro_chi()
        url_start=country_url(country)
        headers['Host']=country_url(country).split("/")[2]
        page = requests.get(url_start+'product-reviews/'+asin+'/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent&pageNumber=1',headers=headers, proxies=proxy)
        review_monitor = {}
        for i in range(10):
            star=Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[1]/a[1]/@title").extract()[i][0:3]
            customer_id=(Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[2]/span/a/@href").extract()[i]).split("/")[3]
            review_time=Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[2]/span[4]/text()").extract()[i][3:]
            review_monitor[i]={'star':star,'customer_id':customer_id,'review_time':review_time}
        print(review_monitor)

    except Exception as e:
        dt = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=30)
        self.retry(eta=dt, exc=e, max_retries=3)