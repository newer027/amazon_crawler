# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-10 08:00
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
            name='UserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('glucose_low', models.PositiveIntegerField(default=60)),
                ('glucose_high', models.PositiveIntegerField(default=180)),
                ('glucose_target_min', models.PositiveIntegerField(default=70)),
                ('glucose_target_max', models.PositiveIntegerField(default=120)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Settings',
            },
        ),
    ]
