#-*- coding:utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib import admin
import datetime

ACCOUNT_TYPE={'free':u'免费账户','bronze':u'付费订阅(bronze)','silver':u'付费订阅(silver)','gold':u'付费订阅(gold)'}

class Bill(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    add_credit = models.PositiveIntegerField(null=True,blank=True)

    # It'll be one of the 4 status ('WAIT_BUYER_PAY', 'WAIT_SELLER_SEND_GOODS',
    # 'WAIT_BUYER_CONFIRM_GOODS', 'TRADE_FINISHED', 'TRADE_CLOSED'), the inital
    # status will be 'INIT'.
    trade_status = models.CharField (max_length=50, default='INIT', null=True)
    created = models.DateTimeField(auto_now_add=True)
    tn = models.SlugField(max_length=6,db_index=True)

    def __str__ (self):
        return (self.user.username+" "+str(self.add_credit))

admin.site.register (Bill)