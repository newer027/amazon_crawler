from celery import Celery
from .models import Shorten_Url
from core.amazon_api import amazon_api
from celery.exceptions import SoftTimeLimitExceeded
from celery.utils.log import get_task_logger
from random import *
from amazon.api import AsinNotFound
import time, re, random, string
from django.contrib.auth.models import User


logger = get_task_logger(__name__)


app = Celery()
app.config_from_object('django.conf:settings')


@app.task(bind=True,time_limit=60,acks_late=True,default_retry_delay=3)
def create_url(self,ItemId,country,seller,user_id,keywords):
    try:

        count=0
        while count<5:
            try:
                count+=1
                amazon = amazon_api(country)
                product=amazon.lookup(ItemId=ItemId)
            except AsinNotFound:
                return 'No_Asin'
            except:
                time.sleep(0.1+random.random()*0.15)
                continue

        rank=str(randint(1,10))
        qid=str(int(time.time()))
        user=User.objects.get(id=user_id)
        for keyword in keywords:
            httpurl = product.detail_page_url+'/ref=sr_1_'+rank+'?ie=UTF8&qid='+qid+'&sr=1-'+rank+'&keywords='+keyword+'&m='+seller
            httpurl = re.sub(r'newer0270b-20','gw004-20',httpurl)
            new_url = Shorten_Url(httpurl = httpurl, shorten_id = get_short_code(),
                        user=user,asin=ItemId,country=country,seller=seller,keywords=keyword)
            new_url.save()

    except SoftTimeLimitExceeded:
        logger.info("Soft Time Limit Exceeded")


def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated id is used then generate next
    while True:
        shorten_id = ''.join(random.choice(char) for x in range(length))
        try:
            Shorten_Url.objects.get(shorten_id=shorten_id)
        except:
            return shorten_id