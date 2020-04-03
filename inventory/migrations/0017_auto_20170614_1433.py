# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-14 06:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_auto_20170612_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='category',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='price_unit',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='inventory_time',
            name='bsr_rank',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventory_time',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory_time',
            name='reviews',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inventory_time',
            name='reviews_add',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inventory_time',
            name='sale_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory_time',
            name='sale_quan',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='inventory',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='inventory_time',
            name='inventory',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]