# Generated by Django 3.0.14 on 2022-03-10 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0032_user_preffered_theme'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='preffered_theme',
            new_name='preferred_theme',
        ),
    ]
