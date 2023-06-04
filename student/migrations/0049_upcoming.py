# Generated by Django 2.2.12 on 2021-09-27 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0048_delete_upcoming'),
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
