# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-28 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follow_sale', '0004_auto_20170428_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_seller',
            name='mark_time',
            field=models.DateTimeField(null=True),
        ),
    ]