# Generated by Django 3.1.7 on 2021-07-24 10:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0081_auto_20210710_2236'),
        ('TTapp', '0050_auto_20210722_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModulesByBloc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('modified_at', models.DateField(auto_now=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.department')),
                ('modules', models.ManyToManyField(blank=True, to='base.Module')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('weeks', models.ManyToManyField(blank=True, to='base.Week')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
