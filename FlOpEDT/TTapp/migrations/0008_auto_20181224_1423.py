# Generated by Django 2.1.4 on 2018-12-24 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20181224_1423'),
        ('TTapp', '0007_auto_20181113_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='stabilize',
            name='fixed_days',
            field=models.ManyToManyField(blank=True, related_name='days_to_fix', to='base.Day'),
        ),
        migrations.AlterField(
            model_name='minhalfdays',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Group'),
        ),
        migrations.AlterField(
            model_name='minhalfdays',
            name='module',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Module'),
        ),
        migrations.AlterField(
            model_name='reasonabledays',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Group'),
        ),
    ]
