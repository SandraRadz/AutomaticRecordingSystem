# Generated by Django 2.1.7 on 2019-05-02 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20190502_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='google_scholar',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]