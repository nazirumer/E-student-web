# Generated by Django 2.2.12 on 2021-09-26 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0046_auto_20210920_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upcoming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2000, null=True)),
                ('description', models.TextField(null=True)),
                ('initial_date', models.DateField(null=True)),
                ('final_date', models.DateField(null=True)),
            ],
        ),
    ]
