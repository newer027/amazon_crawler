# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-27 07:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asin', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=5000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('exist', models.BooleanField(default=True)),
                ('no_exist_time', models.DateTimeField(blank=True)),
                ('no_exist_count', models.IntegerField(blank=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('owner', models.ManyToManyField(blank=True, related_name='follow_sale_product', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['exist', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Product_seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5000)),
                ('seller_id', models.CharField(max_length=250)),
                ('price', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('new', 'new'), ('old', 'old'), ('same', 'same')], default='new', max_length=10)),
                ('flag', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]