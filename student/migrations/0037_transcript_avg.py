# Generated by Django 3.2.7 on 2021-09-17 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0036_auto_20210916_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='avg',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
