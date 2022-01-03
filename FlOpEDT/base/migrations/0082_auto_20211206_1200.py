# Generated by Django 3.1.7 on 2021-12-06 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0030_auto_20210618_1420'),
        ('base', '0081_auto_20210910_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='tutor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taught_courses', to='people.tutor'),
        ),
    ]
