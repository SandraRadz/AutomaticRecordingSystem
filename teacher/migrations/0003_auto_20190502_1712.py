# Generated by Django 2.1.5 on 2019-05-02 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_auto_20190501_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protection',
            name='date_of_confirmation',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='protection',
            name='date_of_pre_protection',
            field=models.DateField(blank=True, null=True),
        ),
    ]