from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
import random
from django.conf import settings


class Inventory(models.Model):
    COUNTRY_CHOICES = (('us', '美国'),('ca', '加拿大'),('fr', '法国'),
                       ('de', '德国'),('it', '意大利'),('jp', '日本'),
                       ('es', '西班牙'),('uk', '英国'),)
    asin = models.CharField(max_length = 100)
    title = models.CharField(max_length = 2000)
    inventory = models.IntegerField(null=True,blank=True,default=0)
    img_url= models.URLField(null=True,max_length=5000)
    detail_page_url = models.URLField(null=True,max_length=5000)
    category = models.CharField(max_length = 1000,null=True,blank=True)
    price_unit = models.CharField(max_length = 100,null=True,blank=True)
    country = models.CharField(max_length=50,choices=COUNTRY_CHOICES,default='us')
    created = models.DateTimeField(blank = True,null = True,auto_now_add=True)
    slug = models.SlugField(max_length = 25,db_index=True,unique=True)
    text = models.CharField(max_length=5000)

    def __str__(self):
        #return self.country,'国家的ASIN',self.asin,'的库存'
        return '%s的商品 %s 的库存' % (self.get_country_display(), self.asin)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.asin+str(random.random())[-3:])
        if not self.text:
            self.text = '%s的商品 %s 的竞品信息' % (self.get_country_display(), self.asin)
        super(Inventory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory:asin_inventory', args=[self.slug])


class Inventory_time(models.Model):
    asin = models.ForeignKey(Inventory,related_name='inventory_time')
    inventory = models.IntegerField(null=True,blank=True,default=0)
    sale_quan = models.PositiveIntegerField(null=True,blank=True,)
    reviews = models.PositiveIntegerField(default=0)
    reviews_add = models.PositiveIntegerField(default=0)
    bsr_rank = models.PositiveIntegerField(null=True,blank=True)
    star = models.CharField(max_length = 50,blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    sale_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(blank = True,null = True,auto_now_add=True)

    class Meta:
        ordering = ['-date']


class Inventory_to_user(models.Model):
    inventory = models.ForeignKey(Inventory,related_name='inventory_to_user')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='inventory_to_user')
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    expired = models.DateTimeField()
