# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-20 06:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
