from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .follow_sale import mail_task,initial_task
from celery import task
from .models import Product
import time


logger = get_task_logger(__name__)

@periodic_task(
    #run_every=(crontab(0, 0,month_of_year='*/3')),
    run_every=(crontab(minute=45,hour='*/3')),
    name="task_save_latest_follow_sale",
    ignore_result=True
)


def task_save_latest_follow_sale():
    for product in Product.objects.all():
        mail_task.delay(product.asin,product.country)
        time.sleep(0.3)
    logger.info("Saved latest follow sale information")

@task
def trigger_initial_task(asin,country):
    initial_task(asin,country)
    logger.info("Initial follow sale")
