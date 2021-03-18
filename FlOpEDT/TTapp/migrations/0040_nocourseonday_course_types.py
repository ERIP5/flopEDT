# Generated by Django 3.0.5 on 2021-03-01 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0065_grouppreferredlinks'),
        ('TTapp', '0039_nocourseonday'),
    ]

    operations = [
        migrations.AddField(
            model_name='nocourseonday',
            name='course_types',
            field=models.ManyToManyField(blank=True, related_name='no_course_on_days', to='base.CourseType'),
        ),
    ]