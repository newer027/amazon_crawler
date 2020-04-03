from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
import random
from django.conf import settings


class Product(models.Model):
    COUNTRY_CHOICES = (('us', '美国'),('ca', '加拿大'),('fr', '法国'),
                       ('de', '德国'),('it', '意大利'),('jp', '日本'),
                       ('es', '西班牙'),('uk', '英国'),)
    asin=models.CharField(max_length=250)
    title=models.CharField(max_length=5000)
    created=models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=50,choices=COUNTRY_CHOICES,default='us')
    img_url= models.URLField(null=True,max_length=5000)
    detail_page_url = models.URLField(null=True,max_length=5000)
    slug=models.SlugField(max_length=250,null=False,blank=False,editable=True,unique=True,db_index=True)
    text = models.CharField(max_length=5000)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('follow_sale:product_detail', args=[self.slug])

    def __str__(self):
        return '%s 的 %s 的跟卖' % (self.get_country_display(), self.asin)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.asin+str(random.randrange(1000)))
        if not self.text:
            self.text = '%s的商品 %s 的跟卖' % (self.get_country_display(), self.asin)
        super(Product, self).save(*args, **kwargs)


class Product_seller(models.Model):
    product = models.ForeignKey(Product,related_name='product_seller')
    name=models.CharField(max_length=5000)
    seller_id=models.CharField(max_length=250)
    price=models.CharField(max_length=50)
    sell_url=models.CharField(max_length=800)
    created=models.DateTimeField(auto_now_add=True)
    flag=models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']


class Seller_change(models.Model):
    product = models.ForeignKey(Product,related_name='seller_change')
    name=models.CharField(max_length=5000)
    seller_id=models.CharField(max_length=250)
    price=models.CharField(max_length=50)
    sell_url=models.CharField(max_length=800)
    created=models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (('new', 'new'),('old', 'old'))
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='new')

    class Meta:
        ordering = ['-created']


class Product_to_user(models.Model):
    product = models.ForeignKey(Product,related_name='product_to_user')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='product_to_user',blank=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    expired = models.DateTimeField()