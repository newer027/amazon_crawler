# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-21 00:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asin_keyword', '0002_asin_keyword_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asin_keyword',
            name='asin',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='asin_keyword',
            name='ean',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='asin_keyword',
            name='keyword',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='asin_keyword',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='asin_keyword',
            name='title',
            field=models.CharField(max_length=2000),
        ),
    ]
