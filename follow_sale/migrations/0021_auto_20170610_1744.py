# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-10 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follow_sale', '0020_merge_20170610_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='detail_page_url',
            field=models.URLField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='product',
            name='img_url',
            field=models.URLField(max_length=5000),
        ),
    ]
