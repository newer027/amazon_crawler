# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-17 06:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asin', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=40, unique=True)),
            ],
            options={
                'ordering': ['asin'],
            },
        ),
        migrations.CreateModel(
            name='Inventory_time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory', models.PositiveIntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('asin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_time', to='inventory.Inventory')),
            ],
        ),
    ]
