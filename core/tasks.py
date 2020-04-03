from inventory.models import Inventory_to_user,Inventory
from keyword_rank.models import Rank_to_user,Rank,Keyword_rank
from asin_keyword.models import Asin_keyword
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.utils import timezone
import datetime
from accounts.models import UserSettings
from .amazon_api import amazon_api_test
from asin_keyword.emails import send_email
import time


logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="remove_expired_and_update_user_status",
    ignore_result=True
)

def remove_expired_and_update_user_status():
    Rank_to_user.objects.filter(expired__lte=timezone.now()).delete()
    Inventory_to_user.objects.filter(expired__lte=timezone.now()).delete()

    for keyword_rank in Keyword_rank.objects.all():
        if not keyword_rank.rank_to_user.all().exists():
            keyword_rank.delete()

    for keyword_rank in Keyword_rank.objects.all():
        if not keyword_rank.rank.all().exists():
            keyword_rank.delete()

    for inventory in Inventory.objects.all():
        if not inventory.inventory_to_user.all().exists():
            inventory.delete()

    for inventory in Inventory.objects.all():
        if not inventory.inventory_time.all().exists():
            inventory.delete()

    for asin_keyword in Asin_keyword.objects.filter(created__lte=timezone.now()-datetime.timedelta(days=1)):
        asin_keyword.delete()

    for user in UserSettings.objects.all():
        user.checked=False
        user.save()
        #if user.valid_to <= timezone.now():
        #    user.status='v0'
        #    user.save()
        #elif user.valid_to <= timezone.now()+datetime.timedelta(days=4):
        #    message = "\n".join([u'{0},您好.'.format(user.user.username),
        #        u'您的AMZ668 VIP还剩{0}即将到期'.format(divmod(user.valid_to-timezone.now(),86400)),
        #        u'如果需要为您的VIP账号续期,请点击amz668.com/recharge'])
        #    send_email(user.email, message, u'您的AMZ668 VIP还剩{0}即将到期'.format(divmod(user.valid_to-timezone.now(),86400)))


@periodic_task(
    run_every=(crontab(minute=40, hour='*/2')),
    name="amazon_api_cron",
    ignore_result=True
)

def amazon_api_cron():
    COUNTRY_CHOICES=(['us','B00OQVZDJM'],['ca','B00QJDU3KY'],['fr','B00QJDO0QC'],['de','B00QJDO0QC'],
                     ['it','B0186FESVC'],['jp','B00QJDOM6U'],['es','B0186FET66'],['uk','B0186FESVC'])
    message=''
    title='失败账号:'

    for i in range(len(COUNTRY_CHOICES)):
        for second in range(3):
            try:
                amazon=amazon_api_test(COUNTRY_CHOICES[i][0],second=second)
                amazon.lookup(ItemId=COUNTRY_CHOICES[i][1])
                time.sleep(0.2)
                #message+='账号%d %s success, ' % (second+1,COUNTRY_CHOICES[i][0])
                #print(message)
            except:
                title+='%s账号%d,' % (COUNTRY_CHOICES[i][0],second+1)
                message+='账号%d %s fail, ' % (second+1,COUNTRY_CHOICES[i][0])
                #print(message)
        message+='\n'
    print(message)
    send_email('amz668@amz668.com', message, title)



"""
from django.utils import timezone
import datetime
from accounts.models import UserSettings
for user in UserSettings.objects.all():
    user.valid_to=timezone.now()+datetime.timedelta(days=8)
"""
