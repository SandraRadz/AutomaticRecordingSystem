# Generated by Django 2.1.5 on 2019-05-03 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_studentgroup_degree'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='google_scholar',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]