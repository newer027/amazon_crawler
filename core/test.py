<<<<<<< HEAD
# -*- coding: utf-8 -*-
=======
from __future__ import print_function
import psutil
def test():
    print("cpu负载:", psutil.cpu_percent(), "%")
    print("内存负载:",psutil.virtual_memory())



>>>>>>> 807e65f54fa12c805bb380ccc606960cb3e3c631




import requests,datetime
from lxml.html import fromstring
from scrapy.selector import Selector


agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Host': "www.amazon.co.jp",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"

    }
s = requests.Session()


def rank_in_web(asin,keyword,country):
    info = {'rank':None,'page':None}
    if country=='us':
        url_start='https://www.amazon.co.jp/s?field-keywords='
        for i in range(5):
            #try:
            page = s.get(url_start+keyword+'&page='+str(i+1),headers=headers)
            print(page.status_code)
            tree = fromstring(page.content)
            print(tree.findtext('.//title'))
            print(len(Selector(text=page.content).xpath('.//li[@class="s-result-item  celwidget "]')))
            print(Selector(text=page.content).xpath('.//*[@id="s-result-count"]/text()').extract())
            item_amount=int((Selector(text=page.content).xpath('.//*[@id="s-result-count"]/text()').extract()[0])[2:4])

            for j in range(len(Selector(text=page.content).xpath('.//li[@class="s-result-item  celwidget "]'))):
                try:
                    seller=(Selector(text=page.content).xpath(".//*[@id='result_"+str(item_amount*i+j)+"']/@data-asin").extract()[0])
                    print(j,seller)
                    #if seller==asin:  //*[@id="result_26"]
                    #    info = {'rank':j+1,'page':i+1}
                    #    print("在类别",node,"下搜索关键词",keyword,":",asin,"排名第",i+1,"页,第",j+1,"名")
                    #    return info
                except:
                    print("发生错误",i,j,16*i+j)
            #except:
            #print("发生错误",i)

def test():
    #rank_in_web('B06ZZCHX6D','phone case',country='us')
    rank_in_web('B06ZZCHX6D','折り畳み傘',country='us')


<<<<<<< HEAD

=======
>>>>>>> 807e65f54fa12c805bb380ccc606960cb3e3c631
"""
from amazon.api import AmazonAPI


def amazon_api(country):
    if country=='us':
        amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')
    elif country == 'ca':
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','newer02703-20',region='CA')
    elif country == 'fr':
        #amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','chengjiante0c-21',region='FR')
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiante0c-21',region='FR')
    elif country == 'de':
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiante06-21',region='DE')
    elif country == 'it':
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiant076-21',region='IT')
    elif country == 'jp':
        amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-22',region="JP")
    elif country == 'es':
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiant04a-21',region='ES')
    else:
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiante00-21',region='UK')
    return amazon

def test():
    #amazon = amazon_api('jp')
    #product = amazon.lookup(ItemId='B018MPAU7W')
    #print(product.ean)


    amazon = amazon_api('fr')
    product = amazon.lookup(ItemId='B000Y8WA38')
    print(product.ean)
"""



#amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiante0c-21',region='FR')



from asin_keyword.emails import send_email
import psutil
import paramiko
def test():


    source_us = '/Users/Jacob/Desktop/amazon_cralwer/amazon_crawler/cookies_am.pkl'
    dest_us = '/home/ubuntu/myprojects/amazon_crawler/cookies_am.pkl'
    source_eu = '/Users/Jacob/Desktop/amazon_cralwer/amazon_crawler/cookies_eu.pkl'
    dest_eu = '/home/ubuntu/myprojects/amazon_crawler/cookies_eu.pkl'
    source_jp = '/Users/Jacob/Desktop/amazon_cralwer/amazon_crawler/cookies_jp.pkl'
    dest_jp = '/home/ubuntu/myprojects/amazon_crawler/cookies_jp.pkl'
    hostname = '119.23.46.230'
    port = 22 # default port for SSH
    username = 'ubuntu'
    password = 'ML#$gbal'
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(source_us, dest_us)
        sftp.put(source_eu, dest_eu)
        sftp.put(source_jp, dest_jp)
    finally:
        t.close()
    send_email('amz668@amz668.com', 'cookie已经保存到服务器!\n服务器CPU负载: %s%%\n内存负载: %s' % (psutil.cpu_percent() ,psutil.virtual_memory()),'自动保存cookie')
"""