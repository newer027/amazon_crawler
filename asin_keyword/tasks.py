from __future__ import print_function
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .cookie_sele import cookie_sele
from celery import task
from .asin_keyword import asin_to_keyword
from .emails import send_email
from .models import Asin_keyword
from datetime import datetime
import psutil,time


logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='0')),
    name="task_save_latest_cookie",
    ignore_result=True,bind=True, default_retry_delay=3, max_retries=3,acks_late = True
)
def task_save_latest_cookie(self):
    line=''
    try:
        cookie_sele('am')
        line+=' am '
    except:
        pass
    try:
        cookie_sele('uk')
        line+=' uk '
    except:
        pass
    try:
        cookie_sele('fr')
        line+=' fr '
    except:
        pass
    try:
        cookie_sele('de')
        line+=' de '
    except:
        pass
    try:
        cookie_sele('it')
        line+=' it '
    except:
        pass
    try:
        cookie_sele('es')
        line+=' es '
    except:
        pass
    try:
        cookie_sele('jp')
        line+=' jp '
    except:
        pass
    send_email('amz668@amz668.com', '%s cookie已经保存到服务器!\n服务器CPU负载: %s%%\n内存负载: %s' % (line, psutil.cpu_percent(), psutil.virtual_memory()),'自动保存cookie')
    logger.info("Saved latest amazon cookie")


@task(bind=True,time_limit=200,acks_late=True,default_retry_delay=3, max_retries=3)
def asin_to_keyword_task(self, asin, country):
    item=asin_to_keyword(asin,country)
    try:
        new_asin = Asin_keyword(asin=asin,img = item['img'],url=item['url'],ean = item['ean'],title=item['title'],keyword = item['keyword'],country=country,created=datetime.now())
        new_asin.save()
    except:
        pass
    return item


@task()
def delete_asin_keyword(asin):
    time.sleep(30)
    Asin_keyword.objects.filter(asin=asin)[0].delete()