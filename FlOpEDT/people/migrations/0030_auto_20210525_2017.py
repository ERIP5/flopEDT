# Generated by Django 3.0.5 on 2021-05-25 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0029_auto_20210511_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='physicalpresence',
            old_name='week_tmp',
            new_name='week',
        ),
    ]
