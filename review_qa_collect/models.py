from django.db import models
from django.conf import settings
from core.models import Product
import time
from core.amazon_api import country_url


class QA_detail(models.Model):
    product = models.ForeignKey(Product,related_name='qa_detail')
    question=models.CharField(max_length=80000)
    answer=models.CharField(max_length=150000,null=True)
    question_chinese=models.CharField(max_length=80000,null=True)
    answer_chinese=models.CharField(max_length=150000,null=True)
    vote=models.IntegerField(null=True,default=0)
    answer_person=models.CharField(max_length=10000,null=True)
    num=models.CharField(max_length=400,null=True)
    answer_url=models.URLField(max_length=100000,null=True)
    created=models.DateTimeField(auto_now_add=True)
    qa_time=models.CharField(max_length=10000,null=True)


class Review_detail(models.Model):
    product = models.ForeignKey(Product,related_name='review_detail')
    created=models.DateTimeField(auto_now_add=True)
    star=models.PositiveIntegerField()
    customer_id=models.CharField(max_length=1000,null=True)
    customer_url=models.CharField(max_length=1000,null=True)
    review_time=models.CharField(max_length=1000)
    review_text=models.CharField(max_length=20000,null=True)
    review_chinese=models.CharField(max_length=20000,null=True)
    normal=models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.customer_url:
            self.customer_url="%sgp/pdp/profile/%s/ref=cm_cr_arp_d_pdp?ie=UTF8" %(country_url(self.product.country),self.customer_id)
        try:
            if self.review_time:
                self.review_time=time.strftime('%Y-%m-%d',time.strptime(self.review_time,'%B %d, %Y'))
        except:
            pass
        super(Review_detail, self).save(*args, **kwargs)
