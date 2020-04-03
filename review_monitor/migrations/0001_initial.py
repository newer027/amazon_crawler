# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-19 01:40
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
                ('country', models.CharField(choices=[('us', '美国'), ('ca', '加拿大'), ('fr', '法国'), ('de', '德国'), ('it', '意大利'), ('jp', '日本'), ('es', '西班牙'), ('uk', '英国')], default='us', max_length=50)),
                ('img_url', models.URLField(max_length=5000, null=True)),
                ('detail_page_url', models.URLField(max_length=5000, null=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('text', models.CharField(max_length=5000)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.PositiveIntegerField()),
                ('customer_id', models.CharField(max_length=1000)),
                ('review_time', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='review_monitor.Product')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Review_to_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('expired', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_to_user', to='review_monitor.Product')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]