# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-21 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_rank', '0009_auto_20170612_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='rank',
            name='sponsored',
            field=models.BooleanField(default=False),
        ),
    ]