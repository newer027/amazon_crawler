from __future__ import print_function
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .cookie_sele import cookie_sele
from celery import task
from .asin_keyword import asin_to_keyword_ca,asin_to_keyword_uk,asin_to_keyword_us,asin_to_keyword_de,asin_to_keyword_fr,asin_to_keyword_it,asin_to_keyword_es,asin_to_keyword_jp
from .emails import send_email
from .models import Asin_keyword
from datetime import datetime
import psutil


logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='0,30')),
    name="task_save_latest_cookie",
    ignore_result=True,bind=True, default_retry_delay=3, max_retries=3,acks_late = True
)
def task_save_latest_cookie(self):
    cookie_sele('am')
    cookie_sele('eu')
    cookie_sele('jp')

    import paramiko
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
    logger.info("Saved latest amazon cookie")


@task(bind=True,time_limit=200,acks_late=True,default_retry_delay=3, max_retries=3)
def asin_to_keyword_task(self, asin, country):
    if country == 'us':
        item=asin_to_keyword_us(asin)
    elif country == 'ca':
        item=asin_to_keyword_ca(asin)
    elif country == 'fr':
        item=asin_to_keyword_fr(asin)
    elif country == 'de':
        item=asin_to_keyword_de(asin)
    elif country == 'it':
        item=asin_to_keyword_it(asin)
    elif country == 'jp':
        item=asin_to_keyword_jp(asin)
    elif country == 'es':
        item=asin_to_keyword_es(asin)
    else:
        item=asin_to_keyword_uk(asin)
    try:
        new_asin = Asin_keyword(asin=asin,img = item['img'],ean = item['ean'],title=item['title'],keyword = item['keyword'],country=country,created=datetime.now())
    except:
        new_asin = Asin_keyword(asin=asin,img = item['img'],ean = item['ean'],title=item['title'],country=country,created=datetime.now())
    new_asin.save()
    return item
