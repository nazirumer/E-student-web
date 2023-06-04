# Generated by Django 3.2.7 on 2021-09-14 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0019_assesment_finished'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='assesment',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='assesment',
            name='course',
        ),
        migrations.RemoveField(
            model_name='assesment',
            name='section',
        ),
        migrations.RemoveField(
            model_name='assesment',
            name='student',
        ),
        migrations.RemoveField(
            model_name='assesment',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='course',
            name='department',
        ),
        migrations.RemoveField(
            model_name='course',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='department',
            name='user',
        ),
        migrations.DeleteModel(
            name='jsoncheck',
        ),
        migrations.RemoveField(
            model_name='section',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='student',
            name='enroll_year',
        ),
        migrations.RemoveField(
            model_name='student',
            name='section',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='department',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='teacherarrangment',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='teacherarrangment',
            name='course',
        ),
        migrations.RemoveField(
            model_name='teacherarrangment',
            name='section',
        ),
        migrations.RemoveField(
            model_name='teacherarrangment',
            name='teacher',
        ),
        migrations.DeleteModel(
            name='Assesment',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.DeleteModel(
            name='Section',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
        migrations.DeleteModel(
            name='TeacherArrangment',
        ),
    ]
