# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-10 01:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_inventory_time_star'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory_time',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='inventory_time',
            name='star',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
