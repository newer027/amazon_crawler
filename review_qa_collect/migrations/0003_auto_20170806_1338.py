# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-06 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review_qa_collect', '0002_auto_20170806_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qa_detail',
            name='answer_url',
            field=models.CharField(max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='qa_detail',
            name='num',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
