# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-04 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='re_qa_slug',
            field=models.SlugField(max_length=250, null=True, unique=True),
        ),
    ]
