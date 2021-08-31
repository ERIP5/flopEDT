# Generated by Django 3.1.7 on 2021-07-02 08:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0030_auto_20210618_1420'),
        ('base', '0079_auto_20210629_1405'),
        ('TTapp', '0052_considerpivots'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleAllCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('modified_at', models.DateField(auto_now=True)),
                ('course_types', models.ManyToManyField(blank=True, to='base.CourseType')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.department')),
                ('groups', models.ManyToManyField(blank=True, to='base.StructuralGroup')),
                ('modules', models.ManyToManyField(blank=True, to='base.Module')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('tutors', models.ManyToManyField(blank=True, to='people.Tutor')),
                ('weeks', models.ManyToManyField(to='base.Week')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NoSimultaneousGroupCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('modified_at', models.DateField(auto_now=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.department')),
                ('groups', models.ManyToManyField(blank=True, to='base.StructuralGroup')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('weeks', models.ManyToManyField(to='base.Week')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConsiderTutorsUnavailability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('modified_at', models.DateField(auto_now=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.department')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('tutors', models.ManyToManyField(blank=True, to='people.Tutor')),
                ('weeks', models.ManyToManyField(to='base.Week')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssignAllCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('modified_at', models.DateField(auto_now=True)),
                ('course_types', models.ManyToManyField(blank=True, to='base.CourseType')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.department')),
                ('groups', models.ManyToManyField(blank=True, to='base.StructuralGroup')),
                ('modules', models.ManyToManyField(blank=True, to='base.Module')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('weeks', models.ManyToManyField(to='base.Week')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
