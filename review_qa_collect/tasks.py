from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from core.models import Product
import time, datetime
from review_qa_collect.reviews_collect import review_collect
from review_qa_collect.qa_collect import qa_collect


logger = get_task_logger(__name__)

@periodic_task(
    #run_every=(crontab(0, 0,month_of_year='*/3')),
    run_every=(crontab(minute=35)),
    name="task_save_latest_re_qa",
    ignore_result=True
)

def task_save_latest_re_qa():
    start = time.time()
    for product in Product.objects.filter(review_qa=True):
        if (time.time()-start)<60*30:
            if not product.review_qa_complete_time:
                review_collect.delay(product.asin,product.country)
                qa_collect.delay(product.asin,product.country)
                time.sleep(10)
            elif product.review_qa_apply_time > product.review_qa_complete_time + datetime.timedelta(days=1):
                review_collect.delay(product.asin,product.country)
                qa_collect.delay(product.asin,product.country)
                time.sleep(10)
    logger.info("Saved latest reviews and QAs")