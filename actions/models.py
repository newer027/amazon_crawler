# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True) #ForeignKey和related_name的用法
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj') #ForeignKey和related_name的用法
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True) #PositiveIntegerField的用法
    target = GenericForeignKey('target_ct', 'target_id') #GenericForeignKey的用法
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True) #auto_now_add的用法
    target_text = models.CharField(max_length=5000)

    class Meta:
        ordering = ('-created',) #ordering的用法
