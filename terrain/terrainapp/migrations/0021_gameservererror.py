# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 03:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrainapp', '0020_sign_calcfinds'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameServerError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=100)),
                ('data', models.CharField(max_length=500)),
                ('message', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'gameservererror',
            },
        ),
    ]