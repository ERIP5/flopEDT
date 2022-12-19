# Generated by Django 3.0.14 on 2022-12-16 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TTapp', '0072_limitsimultaneousroomcourses_max_simultaneous_courses'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='limitsimultaneousroomcourses',
            options={'verbose_name': 'Limit simultaneous courses for rooms', 'verbose_name_plural': 'Limit simultaneous courses for rooms'},
        ),
        migrations.RemoveField(
            model_name='limitsimultaneousroomcourses',
            name='max_simultaneous_courses',
        ),
        migrations.AddField(
            model_name='limitsimultaneousroomcourses',
            name='can_combine_two_groups_if_no_tutor',
            field=models.BooleanField(default=False),
        ),
    ]