# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-28 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follow_sale', '0003_auto_20170427_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='no_exist_count',
            field=models.IntegerField(default=0),
        ),
    ]