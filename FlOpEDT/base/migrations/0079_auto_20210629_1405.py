# Generated by Django 3.1.7 on 2021-06-29 14:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0078_auto_20210618_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='nb',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)], verbose_name='Week number'),
        ),
        migrations.AlterUniqueTogether(
            name='genericgroup',
            unique_together={('name', 'train_prog')},
        ),
    ]
