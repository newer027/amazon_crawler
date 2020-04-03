# -*- coding: utf-8 -*-

import requests,datetime,pytz
from lxml.html import fromstring
from scrapy.selector import Selector
from .models import Rank,Keyword_rank
from core.amazon_api import country_url, pro_chi,USER_AGENTS
from celery import Celery
import random,time


agent = random.choice(USER_AGENTS)
headers = {
    'User-Agent': agent,
    'Host': "www.amazon.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #"Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"
}


app = Celery()
app.config_from_object('django.conf:settings')


@app.task(bind=True,time_limit=500,acks_late=True,default_retry_delay=3, max_retries=3)
def rank_in_web(self,asin,keyword,country='us'):
    try:
        #proxy=pro_chi()
        #proxy=proxies
        info = {'rank':None,'page':None,'sponsored':False}
        keyword_rank=Keyword_rank.objects.filter(asin=asin,country=country,word=keyword)[0]
        url_start=country_url(country)
        headers['Host']=country_url(country).split("/")[2]
        s = requests.Session()
        page = s.get(url_start+'s?field-keywords='+keyword,headers=headers,proxies=pro_chi())
        keyword_rank.rank_url=page.url
        keyword_rank.save()
        if page.status_code != 200:
            raise Exception
        if Selector(text=page.content).xpath('.//*[@id="noResultsTitle"]'):
            raise Exception
        #print(page.status_code, page.text[:200])

        flag_1,flag_2 = True,True
    #//*[@id="s-result-count"] //*[@id="s-result-count"]
        if country=='jp':
            try:
                #len(Selector(text=page.content).xpath('.//li[@class="s-result-item  celwidget "]')) >= \
                #int(Selector(text=page.content).xpath('.//*[@id="s-result-count"]/text()').extract()[0][-4:-2]):
                item_amount=int(Selector(text=page.content).xpath('.//*[@id="s-result-count"]/text()').extract()[0][-4:-2])
            except:
                flag_1 = False
                item_amount=len(Selector(text=page.content).xpath('.//li[@class="s-result-item celwidget "]'))
        else:
            if len(Selector(text=page.content).xpath('.//li[@class="s-result-item celwidget "]')):
                #if len(Selector(text=page.content).xpath('.//li[@class="s-result-item celwidget "]')) >= \
                #int(Selector(text=page.content).xpath('.//*[@id="s-result-count"]/text()').extract()[0][2:4]):
                try:
                    item_amount=int(Selector(text=page.content).xpath('.//*[@id="s-result-count"]/text()').extract()[0][2:4])
                except:
                    flag_1 = False
                    item_amount=len(Selector(text=page.content).xpath('.//li[@class="s-result-item celwidget "]'))
            else:
                flag_2 = False
                #if len(Selector(text=page.content).xpath('.//li[@class="s-result-item s-result-card-for-container a-declarative celwidget "]')) >= \
                #int(Selector(text=page.content).xpath('.//*[@id="s-result-count"]/text()').extract()[0][2:4]):
                try:
                    item_amount=int(Selector(text=page.content).xpath('.//*[@id="s-result-count"]/text()').extract()[0][2:4])
                except:
                    flag_1 = False
                    item_amount=len(Selector(text=page.content).xpath('.//li[@class="s-result-item s-result-card-for-container a-declarative celwidget "]'))


        print(item_amount)
        tree = fromstring(page.content)
        print(tree.findtext('.//title'))
        if tree.findtext('.//title')=='Robot Check' or tree.findtext('.//title')=='Amazon CAPTCHA':
            if len(keyword_rank.rank.all())>2:
                rank=Rank(page=keyword_rank.rank.first().page,number=keyword_rank.rank.first().number,sponsored=keyword_rank.rank.first().sponsored,keyword_rank=keyword_rank)
                rank.save()
                info = {'rank':0,'page':0,'sponsored':True}
                return info
            else:
                rank=Rank(keyword_rank=keyword_rank,page=0,number=0,sponsored=False)
                rank.save()
                info = {'rank':0,'page':0,'sponsored':True}
                return info
    #.//li[@class="s-result-item s-result-card-for-container a-declarative celwidget "]
        if flag_1:
            page_num=0
            while True:
                print(tree.findtext('.//title'),"page",page_num+1)
                if country=='jp':
                    fanwei=range(len(Selector(text=page.content).xpath('.//li[@class="s-result-item  celwidget "]')))
                elif flag_2:
                    fanwei=range(len(Selector(text=page.content).xpath('.//li[@class="s-result-item celwidget "]')))
                else:
                    fanwei=range(len(Selector(text=page.content).xpath('.//li[@class="s-result-item s-result-card-for-container a-declarative celwidget "]')))
                for j in fanwei:
                    #try:
                    if Selector(text=page.content).xpath(".//*[@id='result_"+str(item_amount*page_num+j)+"']/@data-asin"):
                        seller=(Selector(text=page.content).xpath(".//*[@id='result_"+str(item_amount*page_num+j)+"']/@data-asin").extract()[0])
                    else:
                        print("在页面找商品的逻辑错误")
                    print(seller)
                    if seller==asin:
                        try:
                            if (Selector(text=page.content).xpath(".//*[@id='result_"+str(item_amount*page_num+j)+"']/div/div/div/div[2]/h5/text()").extract()[0]).exist():
                                info = {'rank':j+1,'page':page_num+1,'sponsored':True}
                        except:
                            info = {'rank':j+1,'page':page_num+1,'sponsored':False}
                        print("搜索关键词%s:%s排名第%s页,第%s名" % (keyword,asin,page_num+1,j+1))
                        rank=Rank(keyword_rank=keyword_rank,page=info['page'],number=info['rank'],sponsored=info['sponsored'])
                        rank.save()
                        return info
                    #except:
                    #    print('Sponsored:搜索关键词%s,排名第%s页,第%s名' % (keyword,page_num+1,j+1))
                if Selector(text=page.content).xpath(".//*[@id='pagnNextLink']/@href") and page_num<20:
                    time.sleep(2+random.random()*5)

                    while True:
                        try:
                            page = s.get(url_start+(Selector(text=page.content).xpath(".//*[@id='pagnNextLink']/@href")).extract()[0],headers=headers,proxies=pro_chi())
                        except:
                            print("Connection refused by the server..")
                            print("Let me sleep for 5 seconds")
                            print("ZZzzzz...")
                            time.sleep(2+random.random()*5)
                            print("Was a nice sleep, now let me continue...")
                            continue

                    page_num += 1
                else:
                    if len(keyword_rank.rank.all())>2:
                        rank=Rank(page=keyword_rank.rank.first().page,number=keyword_rank.rank.first().number,sponsored=keyword_rank.rank.first().sponsored,keyword_rank=keyword_rank)
                        rank.save()
                        info = {'rank':0,'page':0,'sponsored':False}
                        return info
                    else:
                        rank=Rank(keyword_rank=keyword_rank,page=0,number=0,sponsored=False)
                        rank.save()
                        info = {'rank':0,'page':0,'sponsored':False}
                        return info

        else:
            if country=='jp':
                fanwei=range(len(Selector(text=page.content).xpath('.//li[@class="s-result-item  celwidget "]')))
            elif flag_2:
                fanwei=range(len(Selector(text=page.content).xpath('.//li[@class="s-result-item  celwidget "]')))

            else:
                fanwei=range(len(Selector(text=page.content).xpath('.//li[@class="s-result-item s-result-card-for-container a-declarative celwidget "]')))
            for j in fanwei:
                try:
                    if Selector(text=page.content).xpath(".//*[@id='result_"+str(j)+"']/@data-asin"):
                        seller=(Selector(text=page.content).xpath(".//*[@id='result_"+str(j)+"']/@data-asin").extract()[0])
                    else:
                        print("在页面找商品的逻辑错误")
                    print(seller)
                    if seller==asin:
                        try:
                            if (Selector(text=page.content).xpath(".//*[@id='result_"+str(j)+"']/div/div/div/div[2]/h5/text()").extract()[0])=="sponsored":
                                info = {'rank':j+1,'page':1,'sponsored':True}
                        except:
                            info = {'rank':j+1,'page':1,'sponsored':False}
                        print("搜索关键词%s:%s排名第1页,第%s名" % (keyword,asin,j+1))
                        rank=Rank(keyword_rank=keyword_rank,page=info['page'],number=info['rank'],sponsored=info['sponsored'])
                        rank.save()
                        return info
                except:
                    if len(keyword_rank.rank.all())>2:
                        rank=Rank(page=keyword_rank.rank.first().page,number=keyword_rank.rank.first().number,sponsored=keyword_rank.rank.first().sponsored,keyword_rank=keyword_rank)
                        rank.save()
                        info = {'rank':0,'page':0,'sponsored':False}
                        return info
                    else:
                        rank=Rank(keyword_rank=keyword_rank,page=0,number=0,sponsored=False)
                        rank.save()
                        info = {'rank':0,'page':0,'sponsored':False}
                        return info

    except Exception as e:
        dt = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=40)
        self.retry(eta=dt, exc=e, max_retries=2)

def find_item(amazon,asin):
    item = {}
    product = amazon.lookup(ItemId=asin)
    item['title'] = product.title
    item['img_url'] = product.medium_image_url
    item['detail_page_url'] = product.detail_page_url
    return item


"""
if Selector(text=page.content).xpath(".//*[@id='result_"+str(item_amount*i+j)+"']/div/div/div/div[2]/div[2]/div[1]//a/@href"):
    seller=(Selector(text=page.content).xpath(".//*[@id='result_"+str(item_amount*i+j)+"']/div/div/div/div[2]/div[2]/div[1]//a/@href").extract()[0]).split("/")[5]
elif Selector(text=page.content).xpath(".//*[@id='result_"+str(item_amount*i+j)+"']/div/div[2]/div[1]//a/@href"):
    seller=(Selector(text=page.content).xpath(".//*[@id='result_"+str(item_amount*i+j)+"']/div/div[2]/div[1]//a/@href").extract()[0]).split("/")[5]
elif Selector(text=page.content).xpath(".//*[@id='result_"+str(item_amount*i+j)+"']/div/div[3]/div[1]//a/@href"):
    seller=(Selector(text=page.content).xpath(".//*[@id='result_"+str(item_amount*i+j)+"']/div/div[3]/div[1]//a/@href").extract()[0]).split("/")[5]
"""