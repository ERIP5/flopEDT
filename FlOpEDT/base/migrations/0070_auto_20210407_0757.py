# Generated by Django 3.0.5 on 2021-04-07 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0069_auto_20210402_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='trainingprogramme',
            name='abbrev',
            field=models.CharField(max_length=50),
        ),
    ]