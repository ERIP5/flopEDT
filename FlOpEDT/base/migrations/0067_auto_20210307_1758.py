# Generated by Django 3.0.5 on 2021-03-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0066_auto_20210307_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regen',
            name='fdate',
            field=models.DateField(blank=True, null=True, verbose_name='Regénération complète le'),
        ),
        migrations.AlterField(
            model_name='regen',
            name='sdate',
            field=models.DateField(blank=True, null=True, verbose_name='Regénération stabilisée le'),
        ),
    ]
