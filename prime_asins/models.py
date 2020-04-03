from django.db import models


class Asin_detail(models.Model):
    sell_rank = models.IntegerField(verbose_name=u"销售额排行", blank=True, null=True)
    sell_quant = models.IntegerField(verbose_name=u"销售数量", blank=True, null=True)
    sell_amount = models.IntegerField(verbose_name=u"销售额", blank=True, null=True)
    fu_sell_quant = models.IntegerField(verbose_name=u"父体销售数量", blank=True, null=True)
    fu_sell_amout = models.IntegerField(verbose_name=u"父体销售额", blank=True, null=True)

    COUNTRY_CHOICES = (('us', '美国'),('ca', '加拿大'),('fr', '法国'),
                       ('de', '德国'),('it', '意大利'),('jp', '日本'),
                       ('es', '西班牙'),('uk', '英国'),)

    country = models.CharField(verbose_name=u'国别', choices=COUNTRY_CHOICES, max_length=60, default="us")

    img_url= models.URLField(null=True,verbose_name=u"图片", max_length=5000)
    detail_page_url = models.URLField(null=True,verbose_name=u"网页", max_length=5000)
    price = models.CharField(max_length=50,verbose_name=u"价格", null = True)
    brand = models.CharField(max_length=500,verbose_name=u"品牌", null = True)
    label = models.CharField(max_length=500,verbose_name=u"标牌", null = True)
    bsr_rank = models.PositiveIntegerField(null=True,verbose_name=u"排名", blank=True)
    description = models.CharField(max_length=1000, verbose_name=u"描述", blank=False, null=True)
    asin = models.CharField(max_length=200, verbose_name=u"ASIN", blank=True, null=True)
    title = models.CharField(max_length=1000, verbose_name=u"标题", blank=True, null=True)
    fu_asin = models.CharField(max_length=200, verbose_name=u"父体ASIN", blank=True, null=True)
    fu_asin_title = models.CharField(max_length=1000, verbose_name=u"父体ASIN标题", blank=True, null=True)
    created = models.DateTimeField(blank = True,null = True,auto_now_add=True)

    class Meta:
        ordering = ['description','sell_rank']

    def __str__(self):
        return '%s的商品 %s 的详情' % (self.get_country_display(), self.asin)


class ImportFile(models.Model):

    file = models.FileField(upload_to='static/documents/')
    name = models.CharField(max_length=500, verbose_name=u'文件名')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name