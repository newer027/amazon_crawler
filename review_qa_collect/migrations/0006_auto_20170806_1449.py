# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-06 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review_qa_collect', '0005_auto_20170806_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qa_detail',
            name='answer',
            field=models.CharField(max_length=150000, null=True),
        ),
        migrations.AlterField(
            model_name='qa_detail',
            name='answer_person',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='qa_detail',
            name='answer_url',
            field=models.URLField(max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='qa_detail',
            name='num',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='qa_detail',
            name='qa_time',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='qa_detail',
            name='question',
            field=models.CharField(max_length=80000),
        ),
    ]