# Generated by Django 5.1.3 on 2024-11-18 23:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_alter_attendance_status'),
        ('courses', '0003_remove_course_code_course_instructor_and_more'),
        ('students', '0004_rename_enrollment_date_student_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('student', 'course', 'date')},
        ),
    ]
