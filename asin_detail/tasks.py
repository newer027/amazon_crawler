from asin_detail.asin_detail import asin_to_detail
import time
from core.models import Product
from review_qa_collect.models import Review_detail,QA_detail
from review_qa_collect.reviews_collect import translate
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="asins_depart",
    ignore_result=True
)


def asins_depart():
    logger.info("Saved latest asins_depart")
    start = time.time()
    for asin_detail in Product.objects.filter(title=""):
        if (time.time()-start)<60:
            asin_to_detail.delay(asin_detail.asin,asin_detail.country)
            time.sleep(0.16)
    """
    for review_detail in Review_detail.objects.filter(review_chinese=None):
        if (time.time()-start)<60:
            if review_detail.product.country in ['de','it','jp']:
                fromLang = review_detail.product.country
            elif review_detail.product.country =='fr':
                fromLang = 'fra'
            elif review_detail.product.country =='es':
                fromLang = 'spa'
            else:
                fromLang = 'en'
            review_detail.review_chinese=translate(review_detail.review_text,fromLang)
            review_detail.save()
            time.sleep(1)

    for qa_detail in QA_detail.objects.filter(question_chinese=None):
        if (time.time()-start)<60:
            if qa_detail.product.country in ['de','it','jp']:
                fromLang = qa_detail.product.country
            elif qa_detail.product.country =='fr':
                fromLang = 'fra'
            elif qa_detail.product.country =='es':
                fromLang = 'spa'
            else:
                fromLang = 'en'
            if qa_detail.question:
                question_chinese=translate(qa_detail.question,fromLang)
                qa_detail.question_chinese=question_chinese
                print(question_chinese)
                time.sleep(1)
            if qa_detail.answer.strip()!="" and not qa_detail.answer_chinese:
                answer_chinese=translate(qa_detail.answer,fromLang)
                qa_detail.answer_chinese=answer_chinese
                print(answer_chinese)
                time.sleep(1)
            qa_detail.save()
        #print(question_chinese,answer_chinese)
    """