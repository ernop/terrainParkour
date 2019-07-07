# Generated by Django 2.2 on 2019-07-07 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terrainparkour', '0005_auto_20190706_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionresultsent',
            name='user',
            field=models.ForeignKey(db_column='userid', default=None, on_delete=django.db.models.deletion.CASCADE, related_name='actionresultssent', to='terrainparkour.RobloxUser'),
        ),
        migrations.AlterField(
            model_name='badgegrant',
            name='badge',
            field=models.ForeignKey(db_column='badgeid', on_delete=django.db.models.deletion.CASCADE, related_name='badgegrants', to='terrainparkour.Badge'),
        ),
        migrations.AlterField(
            model_name='badgegrant',
            name='user',
            field=models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.CASCADE, related_name='badgegrants', to='terrainparkour.RobloxUser'),
        ),
        migrations.AlterField(
            model_name='bestrun',
            name='race',
            field=models.ForeignKey(db_column='raceid', on_delete=django.db.models.deletion.CASCADE, related_name='bestruns', to='terrainparkour.Race'),
        ),
        migrations.AlterField(
            model_name='bestrun',
            name='user',
            field=models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.CASCADE, related_name='bestruns', to='terrainparkour.RobloxUser'),
        ),
    ]