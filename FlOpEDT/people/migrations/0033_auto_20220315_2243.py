# Generated by Django 3.0.14 on 2022-03-15 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0032_tutorpreference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='max_hours_per_day',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='pref_hours_per_day',
        ),
    ]
