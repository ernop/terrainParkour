# Generated by Django 2.2 on 2019-07-07 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrainparkour', '0004_auto_20190706_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionresultsent',
            name='notifyAllExcept',
            field=models.BooleanField(db_column='notifyallexcept'),
        ),
        migrations.AlterField(
            model_name='badge',
            name='assetId',
            field=models.IntegerField(db_column='assetid'),
        ),
        migrations.AlterField(
            model_name='bestrun',
            name='raceMilliseconds',
            field=models.IntegerField(db_column='racemilliseconds'),
        ),
    ]