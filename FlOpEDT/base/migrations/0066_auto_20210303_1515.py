# Generated by Django 3.0.13 on 2021-03-03 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0022_auto_20201001_0727'),
        ('base', '0065_grouppreferredlinks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='abbrev',
            field=models.CharField(max_length=10, verbose_name='intitulé abbrégé'),
        ),
        migrations.AlterField(
            model_name='module',
            name='head',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='people.Tutor', verbose_name='responsable'),
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='nom complet'),
        ),
    ]
