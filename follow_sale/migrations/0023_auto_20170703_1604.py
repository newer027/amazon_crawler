# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-03 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follow_sale', '0022_auto_20170612_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_seller',
            name='sell_url',
            field=models.CharField(default='http://www.amz668.com/follow_sale/', max_length=800),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seller_change',
            name='sell_url',
            field=models.CharField(default='http://www.amz668.com/follow_sale/', max_length=800),
            preserve_default=False,
        ),
    ]
