from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
import random
from django.conf import settings
from core.amazon_api import country_url


class Product(models.Model):
    COUNTRY_CHOICES = (('us', '美国'),('ca', '加拿大'),('fr', '法国'),
                       ('de', '德国'),('it', '意大利'),('jp', '日本'),
                       ('es', '西班牙'),('uk', '英国'),)
    STAR_CHOICES = ((1, '1星'),(2, '2星和以下'),(3, '3星和以下'))
    asin=models.CharField(max_length=250)
    title=models.CharField(max_length=5000)
    created=models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=50,choices=COUNTRY_CHOICES,default='us')
    star = models.PositiveIntegerField(choices=STAR_CHOICES,default=1)
    img_url= models.URLField(null=True,max_length=5000)
    detail_page_url = models.URLField(null=True,max_length=5000)
    slug=models.SlugField(max_length=250,null=False,blank=False,editable=True,unique=True,db_index=True)
    text = models.CharField(max_length=5000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='review_to_user',blank=True)
    updated = models.DateTimeField(auto_now=True)
    expired = models.DateTimeField()

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('follow_sale:product_detail', args=[self.slug])

    def __str__(self):
        return '%s 的 %s 的防差评' % (self.get_country_display(), self.asin)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.asin+str(random.randrange(1000)))
        if not self.text:
            self.text = '%s的商品 %s 的防差评' % (self.get_country_display(), self.asin)
        super(Product, self).save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(Product,related_name='review')
    star=models.PositiveIntegerField()
    customer_id=models.CharField(max_length=1000)
    customer_url=models.CharField(max_length=1000)
    review_time=models.CharField(max_length=1000)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.customer_url:
            self.customer_url="%sgp/pdp/profile/%s/ref=cm_cr_arp_d_pdp?ie=UTF8" %(country_url(self.product.country),self.customer_id)
        super(Review, self).save(*args, **kwargs)