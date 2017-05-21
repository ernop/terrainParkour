# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 18:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terrainapp', '0003_auto_20170520_0802'),
    ]

    operations = [
        migrations.CreateModel(
            name='BestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('raceMilliseconds', models.IntegerField()),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bestruns', to='terrainapp.Race')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bestruns', to='terrainapp.RobloxUser')),
            ],
            options={
                'db_table': 'bestrun',
            },
        ),
    ]