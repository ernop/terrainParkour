# Generated by Django 2.2 on 2019-07-07 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrainparkour', '0011_auto_20190706_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robloxuser',
            name='banLevel',
            field=models.IntegerField(db_column='banlevel', default=0),
        ),
    ]
