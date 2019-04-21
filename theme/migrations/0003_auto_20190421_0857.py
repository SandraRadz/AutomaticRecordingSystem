# Generated by Django 2.1.5 on 2019-04-21 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0002_auto_20190412_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writework',
            name='english_work_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='writework',
            name='work_name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='writework',
            name='year_of_work',
            field=models.SmallIntegerField(default=2019),
        ),
    ]
