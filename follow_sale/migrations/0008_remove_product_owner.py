# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-06 03:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('follow_sale', '0007_product_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='owner',
        ),
    ]
