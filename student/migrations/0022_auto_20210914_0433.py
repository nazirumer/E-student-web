# Generated by Django 3.2.7 on 2021-09-14 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_assesment_course_department_grade_jsoncheck_section_student_teacher_teacherarrangment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assesment',
            name='semister',
            field=models.CharField(choices=[('semisterI', 'semisterI'), ('semisterII', 'semisterII')], default='semisterI', max_length=200),
        ),
        migrations.AddField(
            model_name='teacherarrangment',
            name='semister',
            field=models.CharField(choices=[('semisterI', 'semisterI'), ('semisterII', 'semisterII')], default='semisterI', max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='assesment',
            unique_together={('course', 'student', 'semister')},
        ),
    ]
