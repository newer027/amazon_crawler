from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
import random


class Keyword_rank(models.Model):
    COUNTRY_CHOICES = (('us', '美国'),('ca', '加拿大'),('fr', '法国'),
                       ('de', '德国'),('it', '意大利'),('jp', '日本'),
                       ('es', '西班牙'),('uk', '英国'),)
    asin = models.CharField(max_length = 400)
    title = models.CharField(max_length = 5000)
    country = models.CharField(max_length=50,choices=COUNTRY_CHOICES,default='us')
    word = models.CharField(max_length = 5000,null=True)
    rank_url = models.URLField(null=True,max_length=5000)
    img_url= models.URLField(null=True,max_length=5000)
    detail_page_url = models.URLField(null=True,max_length=5000)
    created = models.DateTimeField(blank = True,null = True,auto_now_add=True)
    slug = models.SlugField(max_length = 40,db_index=True,unique=True)
    text = models.CharField(max_length=5000)

    def __str__(self):
        return '%s的商品 %s 在关键词 %s 下的排名' % (self.get_country_display(), self.asin,self.word)


    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.asin+str(random.random())[-3:])
        if not self.text:
            self.text = '%s的商品 %s 在关键词 %s 下的排名' % (self.get_country_display(), self.asin,self.word)
        super(Keyword_rank, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('keyword_rank:rank_detail', args=[self.slug])


class Rank(models.Model):
    keyword_rank = models.ForeignKey(Keyword_rank,related_name='rank')
    page = models.PositiveIntegerField(null=True,blank=True)
    number = models.PositiveIntegerField(null=True,blank=True)
    to = models.PositiveIntegerField(null=True,blank=True)
    sponsored=models.BooleanField(default=False)
    created = models.DateTimeField(blank = True,null = True,auto_now_add=True)
    text = models.CharField(max_length=5000)

    def save(self, *args, **kwargs):
        if not self.text:
            if not self.page and not self.number:
                self.text = '%s页内没有找到' % (self.to)
            else:
                self.text = '第%s页,第%s名' % (self.page, self.number)
        super(Rank, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']


class Rank_to_user(models.Model):
    keyword_rank = models.ForeignKey(Keyword_rank,related_name='rank_to_user')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='rank_to_user')
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    expired = models.DateTimeField()
