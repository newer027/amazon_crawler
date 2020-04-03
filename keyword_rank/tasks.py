from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from keyword_rank.keyword_rank import rank_in_web
from keyword_rank.models import Keyword_rank
import time,datetime
from django.utils import timezone


logger = get_task_logger(__name__)

@periodic_task(
    #run_every=(crontab(0, 0,month_of_year='*/3')),
    run_every=(crontab(minute=25,hour='*/2')),
    name="task_save_latest_rank",
    ignore_result=True
)
def task_save_latest_rank():
    start = time.time()
    for keyword_rank in Keyword_rank.objects.all():
        if not keyword_rank.rank.filter(created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone())) and (time.time()-start)<60*60*1.5:
            rank_in_web.delay(keyword_rank.asin,keyword_rank.word,keyword_rank.country)
            print(keyword_rank.asin,keyword_rank.word)
            time.sleep(1)
    for keyword_rank in Keyword_rank.objects.all():
        if len(keyword_rank.rank.filter(sponsored=True,created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone())))>1:
            keyword_rank.rank.filter(created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone()))[0].delete()
        elif len(keyword_rank.rank.filter(sponsored=False,created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone())))>1:
            keyword_rank.rank.filter(created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone()))[0].delete()

    logger.info("Saved latest rank")

#-datetime.timedelta(days=1)

"""
for keyword_rank in Keyword_rank.objects.all():
    if len(keyword_rank.rank.filter(sponsored=True,created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone())))==2:
        keyword_rank.rank.filter(created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone()))[0].delete()
    elif len(keyword_rank.rank.filter(sponsored=False,created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone())))==2:
        keyword_rank.rank.filter(created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone()))[0].delete()



from keyword_rank.models import Keyword_rank
from keyword_rank.keyword_rank import rank_in_web

i=1
for keyword_rank in Keyword_rank.objects.all():
    try:
        if keyword_rank.rank.filter(created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone()))[0].page==0:
            rank_in_web.delay(keyword_rank.asin,keyword_rank.word,keyword_rank.country)
            time.sleep(10)
            #print("rank_in_web('%s','%s','%s')" % (keyword_rank.asin,keyword_rank.word,keyword_rank.country))
    except:
        pass
        #print('sleep(10)')
        #i+=1
        #keyword_rank.rank.filter(created__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone()))[1].delete()
        #time.sleep(10)
"""
