from django.db import models


class In_word(models.Model):
    COUNTRY_CHOICES = (('us', '美国'),('ca', '加拿大'),('fr', '法国'),
                       ('de', '德国'),('it', '意大利'),('jp', '日本'),
                       ('es', '西班牙'),('uk', '英国'),)
    in_word = models.CharField(max_length = 1000)
    country = models.CharField(max_length=50,choices=COUNTRY_CHOICES,default='us')


class Out_word(models.Model):
    in_out = models.ForeignKey(In_word,related_name='out_word')
    out_word = models.CharField(max_length = 1000)