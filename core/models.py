from django.db import models
from ckeditor.fields import RichTextField
from django.core.urlresolvers import reverse
from django.utils.text import slugify
import random
from django.conf import settings


class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating 'created' and 'modified'
    fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(models.Model):
    content = RichTextField()


class Product(models.Model):
    COUNTRY_CHOICES = (('us', '美国'),('ca', '加拿大'),('fr', '法国'),
                       ('de', '德国'),('it', '意大利'),('jp', '日本'),
                       ('es', '西班牙'),('uk', '英国'),)
    asin = models.CharField(max_length = 400)
    asins_in = models.TextField()
    title = models.CharField(max_length = 5000)
    created = models.DateTimeField(blank = True,null = True,auto_now_add=True)
    brand = models.CharField(max_length=500,null = True)
    country = models.CharField(max_length=50,choices=COUNTRY_CHOICES,default='us')
    img_url= models.URLField(null=True,max_length=5000)
    detail_page_url = models.URLField(null=True,max_length=5000)
    price = models.CharField(max_length=50,null = True)
    re_qa_slug=models.SlugField(max_length=250,null=True,blank=False,editable=True,unique=True)
    updated = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length=500,null = True)
    bsr_rank = models.PositiveIntegerField(null=True,blank=True)
    text = models.CharField(max_length=2000)
    review_qa = models.BooleanField(default=False)
    detail = models.BooleanField(default=False)
    review_qa_apply_time = models.DateTimeField(null=True)
    review_qa_complete_time = models.DateTimeField(null=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='product_review_qa_to_user',blank=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='asin_detail',blank=True)

    def __str__(self):
        if self.review_qa:
            return '%s 的 %s 的问答和评论' % (self.get_country_display(), self.asin)
        else:
            return '%s的商品 %s 的详情' % (self.get_country_display(), self.asin)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        if self.review_qa:
            return reverse('review_qa_collect:product_detail', args=[self.re_qa_slug])

    def save(self, *args, **kwargs):
        if self.review_qa and not self.re_qa_slug:
            self.re_qa_slug = slugify(self.asin+str(random.randrange(1000)))
        if not self.text:
            if self.review_qa:
                self.text = '%s的商品 %s 的问答和评论' % (self.get_country_display(), self.asin)
            else:
                self.text = '%s的商品 %s 的详情' % (self.get_country_display(), self.asin)
        super(Product, self).save(*args, **kwargs)


class Product_to_user(models.Model):
    asin = models.ForeignKey(Product,related_name='Product_to_User')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='Product_to_User',blank=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    review_qa = models.BooleanField(default=False)
    detail = models.BooleanField(default=False)