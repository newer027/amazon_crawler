from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
import random


class Asin_keyword(models.Model):
    COUNTRY_CHOICES = (('us', '美国'),('ca', '加拿大'),('fr', '法国'),
                       ('de', '德国'),('it', '意大利'),('jp', '日本'),
                       ('es', '西班牙'),('uk', '英国'),)
    asin = models.CharField(max_length = 100)
    title = models.CharField(max_length = 2000)
    ean = models.CharField(max_length = 100,null = True)
    keyword = models.CharField(max_length = 5000,null = True)
    img = models.URLField(null=True,max_length=5000)
    url = models.CharField(max_length = 5000)
    country = models.CharField(max_length=50,choices=COUNTRY_CHOICES,default='us')
    created = models.DateTimeField(blank = True,null = True,auto_now_add=True)
    slug = models.SlugField(max_length = 100,db_index=True,unique=True)
    text = models.CharField(max_length=5000)

    def __str__(self):
        #return self.country,'国家的ASIN',self.asin,'的SEARCH TERMS'
        return '%s的商品 %s 的SEARCH TERMS' % (self.get_country_display(), self.asin)

    class Meta:
        ordering = ['asin']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.asin+str(random.random())[-3:])
        if not self.text:
            self.text = '%s的商品 %s 的SEARCH TERMS' % (self.get_country_display(), self.asin)
        super(Asin_keyword, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('asin_keyword:asin_keyword', args=[self.slug])


