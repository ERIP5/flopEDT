# Generated by Django 3.0.14 on 2022-06-18 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservationperiodicity',
            old_name='bm_y_choice',
            new_name='bm_day_choice',
        ),
        migrations.RenameField(
            model_name='reservationperiodicity',
            old_name='bw_weeks_nb',
            new_name='bw_weeks_interval',
        ),
        migrations.AlterField(
            model_name='reservationperiodicity',
            name='bm_x_choice',
            field=models.CharField(blank=True, choices=[(1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (-2, 'Ante Last'), (-1, 'Last')], max_length=2, null=True),
        ),
    ]
