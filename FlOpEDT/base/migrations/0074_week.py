# Generated by Django 3.0.5 on 2021-05-10 18:01

import django.core.validators
from django.db import migrations, models


def add_all_weeks(apps, schema_editor):
    Week = apps.get_model('base', 'Week')
    for y in range(10, 51):
        year = 2000+y
        if y in {20, 26, 32, 37, 48}:
            final_week = 53
        else:
            final_week = 52
        for w_nb in range(1, final_week+1):
            Week.objects.get_or_create(nb=w_nb, year=year)
    Week.objects.get_or_create(nb=0, year=0)
    Week.objects.get_or_create(nb=1, year=0)


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0073_auto_20210426_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('year', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.RunPython(add_all_weeks),
    ]
