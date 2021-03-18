# Generated by Django 3.0.5 on 2020-07-08 15:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0056_moduletutorrepartition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.CreateModel(
            name='VisioPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=8, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)])),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='visio_pref', to='base.Course')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledCourseAdditional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, default=None, null=True)),
                ('scheduled_course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='additional', to='base.ScheduledCourse')),
            ],
        ),
    ]