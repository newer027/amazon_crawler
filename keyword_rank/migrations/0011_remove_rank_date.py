# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-22 03:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_rank', '0010_rank_sponsored'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rank',
            name='date',
        ),
    ]
