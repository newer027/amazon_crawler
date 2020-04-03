# //*[@class="a-section review"]
# https://www.amazon.co.jp/product-reviews/B01KJR7772/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent&pageNumber=1
# //*[@class="a-section review"]/div[1]/a[1]/i/span
# //*[@class="a-section review"]/div[2]/span[1]//a/@href
# //*[@class="a-section review"]/div[2]/span[4]


import datetime
from scrapy.selector import Selector
from .models import Product, Review
from core.amazon_api import get_url
from celery import Celery
from django.utils import timezone
from asin_keyword.emails import send_email


app = Celery()
app.config_from_object('django.conf:settings')


@app.task(bind=True,time_limit=500,acks_late=True,default_retry_delay=3, max_retries=3)
def review_monitor(self,asin,country,comp_star,crontab=False):

    product=Product.objects.filter(asin=asin)[0]
    url_add='product-reviews/'+asin+'/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent&pageNumber=1'
    page=get_url(url_add,country=country)
    if not page:
        return '没有打开页面'

    #tree = fromstring(page.content)
    #print(tree.findtext('.//title'),page.content)
    review_monitors = {}
    try:
        for i in range(10):
            star=int(Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[1]/a[1]/@title").extract()[i][0:1])
            customer_id=(Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[2]/span//a/@href").extract()[i]).split("/")[4]
            review_time=Selector(text=page.content).xpath(".//*[@class='a-section review']/div/div[2]/span[4]/text()").extract()[i][3:]
            if star <= comp_star:
                review_monitors[customer_id]={'star':star,'customer_id':customer_id,'review_time':review_time}
        print(review_monitors)
    except:
        return '商品没有评论'

    if not crontab:
        for customer_id in review_monitors:
            review=Review(product=product,star=review_monitors[customer_id]['star'],customer_id=customer_id,review_time=review_monitors[customer_id]['review_time'])
            review.save()
    else:
        change=False
        for customer_id in review_monitors:
            if not Review.objects.filter(product=product,customer_id=customer_id,review_time=review_monitors[customer_id]['review_time']):
                change=True
                review=Review(product=product,star=review_monitors[customer_id]['star'],customer_id=customer_id,review_time=review_monitors[customer_id]['review_time'])
                review.save()
        if change:
            user=product.user
            reviews = Review.objects.filter(product=product, created__gte=timezone.now()-datetime.timedelta(minutes=3))
            customer_ids = reviews.values_list('customer_id', flat=True)
            message = "\n".join([u'{0},您好.'.format(user.username), '{0}有差评出现:'.format(product.title),u'评论人:',
                ','.join([customer_id for customer_id in customer_ids]),u'评论详情:','/'.join(['amz668.com/review_monitor',product.slug]),
                u'直达亚马逊:{0}'.format(page.url)])
            send_email(user.email, message, '您跟踪的商品出现新的差评')
