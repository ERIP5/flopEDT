# Generated by Django 2.1.4 on 2019-11-27 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0039_auto_20191122_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependency',
            name='course1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_course', to='base.Course'),
        ),
        migrations.AlterField(
            model_name='dependency',
            name='course2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_course', to='base.Course'),
        ),
    ]
