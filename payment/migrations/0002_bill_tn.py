# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-29 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='tn',
            field=models.SlugField(default=0, max_length=6),
            preserve_default=False,
        ),
    ]