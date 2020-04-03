from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


# Create your models here.
class Shorten_Url(models.Model):
    COUNTRY_CHOICES = (('us', '美国'),('ca', '加拿大'),('fr', '法国'),
                       ('de', '德国'),('it', '意大利'),('jp', '日本'),
                       ('es', '西班牙'),('uk', '英国'),)
    asin=models.CharField(max_length=250)
    seller=models.CharField(max_length=250)
    country=models.CharField(max_length=50,choices=COUNTRY_CHOICES,default='us')
    keywords = models.TextField()
    text = models.CharField(max_length=5000)
    shorten_id = models.SlugField(max_length=6,db_index=True)
    httpurl = models.URLField(max_length=2000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='url',blank=True)
    pub_date = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return '%s的商品 %s 的超链' % (self.get_country_display(), self.asin)

    class Meta:
        ordering = ['-pub_date']

    def get_absolute_url(self):
        return reverse('shorten_url:url_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.text:
            self.text = '%s的商品 %s 的超链' % (self.get_country_display(), self.asin)
        super(Shorten_Url, self).save(*args, **kwargs)


