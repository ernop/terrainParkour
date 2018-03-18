# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-17 21:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terrainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tixtransaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tixtransactions', to='terrainapp.RobloxUser'),
        ),
    ]
