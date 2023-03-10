# Generated by Django 3.0.5 on 2020-09-15 10:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0059_courseadditional'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnrichedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('description', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='scheduledcourseadditional',
            name='url',
        ),
        migrations.AddField(
            model_name='courseadditional',
            name='visio_preference_value',
            field=models.SmallIntegerField(default=8, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)]),
        ),
        migrations.AlterField(
            model_name='scheduledcourse',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Room'),
        ),
        migrations.AddField(
            model_name='scheduledcourseadditional',
            name='links',
            field=models.ManyToManyField(related_name='additionnal_set', to='base.EnrichedLink'),
        ),
    ]
