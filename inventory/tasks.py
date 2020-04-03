from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from inventory.models import Inventory
from inventory.inventory import inventory_query
import time,datetime
from django.utils import timezone


logger = get_task_logger(__name__)

@periodic_task(
    #run_every=(crontab(0, 0,month_of_year='*/3')),
    run_every=(crontab(minute=0, hour='*/3')),
    name="task_save_latest_inventory",
    ignore_result=True)


def task_save_latest_inventory():
    start = time.time()
    for inventory in Inventory.objects.all(): #filter(country__in=['it', 'es', 'jp','ca']):
        if not inventory.inventory_time.filter(date__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone()))\
                and (time.time()-start)<60*60*3:
            inventory_query.delay(inventory.asin,inventory.country,crontab=True)
            time.sleep(3)
        if len(inventory.inventory_time.filter(date__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone())))>1:
            inventory.inventory_time.filter(date__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone()))[0].delete()
    logger.info("Saved latest inventory")


"""
@task()
def inventory_query_task(asin,country):
    #amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')
    #inventory_query(amazon,new_asin.asin)
    #new_asin.title = item['title']
    #new_asin.save()
    #inventory_time = Inventory_time(asin=new_asin,inventory=item['quantity'],date=datetime.now())
    #inventory_time.save()
    inventory_query(asin,country)


positions_change = Positions_change(
    portfolio=Portfolio.objects.filter(slug=portfilio)[0],
    time= datetime.fromtimestamp(data[u'list'][i]['updated_at'] / 1000),
    name=ZHs0[url_ap0],
    code=url_ap0,
    detail=detail
)
positions_change.save()

today = datetime.datetime.now()
p1 = datetime.timedelta(days=1)
users_today = lockoutusers.objects.filter(lockouttime__range=[today.date(),(today+p1).date()])
"""

"""
Saves latest image from Flickr
for inventory in Inventory.objects.all():
    try:
        item = inventory_query(amazon,inventory.asin)
        new_inventory=Inventory_time(asin=inventory,inventory = item['quantity'],date = datetime.now())
        new_inventory.save()
    except:
        inventory.inventory = 0
        inventory.save()

for inventory in Inventory.objects.all():
    if inventory.inventory_time.filter(date__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone())):
        if inventory.inventory_time.filter(date__gte=timezone.make_aware(datetime.datetime.combine(datetime.datetime.now().date(), datetime.time()), timezone.get_current_timezone()))[0].reviews==0:
            get_reviews.delay(inventory.country,inventory.asin,crontab=True)
            time.sleep(0.3)

"""

#jobs = group(inventory_query.s(inventory.asin,inventory.country,crontab=True) for inventory in Inventory.objects.all())
#jobs.apply_async()
