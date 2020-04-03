from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .review_monitor import review_monitor
from celery import task
from .models import Product
import time


logger = get_task_logger(__name__)

@periodic_task(
    #run_every=(crontab(0, 0,month_of_year='*/3')),
    run_every=(crontab(minute=10,hour='*/3')),
    name="task_save_latest_review_monitor",
    ignore_result=True
)


def task_save_latest_review_monitor():
    for product in Product.objects.all():
        review_monitor.delay(product.asin,product.country,product.star,crontab=True)
        time.sleep(0.3)
    logger.info("Saved latest review monitor information")

@task
def trigger_initial_task(asin,country,star):
    review_monitor(asin,country,star)
    logger.info("Initial review monitor")
