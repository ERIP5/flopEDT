# Generated by Django 2.1.3 on 2018-11-26 14:41

from django.db import migrations, models

def translate_slot_preferences(apps, schema_editor):
    Slot = apps.get_model('base', 'Slot')
    UserPreference = apps.get_model('base', 'UserPreference')
    CoursePreference = apps.get_model('base', 'CoursePreference')
    RoomPreference = apps.get_model('base', 'RoomPreference')
    for pref in UserPreference.objects.all():
        pref.day = pref.creneau.jour.day
        pref.start_time = pref.creneau.heure.hours*60 + pref.creneau.heure.minutes
        pref.duration = pref.creneau.duration
        pref.save()
    for pref in CoursePreference.objects.all():
        pref.day = pref.creneau.jour.day
        pref.start_time = pref.creneau.heure.hours*60 + pref.creneau.heure.minutes
        pref.duration = pref.creneau.duration
        pref.save()
    for pref in RoomPreference.objects.all():
        pref.day = pref.creneau.jour.day
        pref.start_time = pref.creneau.heure.hours*60 + pref.creneau.heure.minutes
        pref.duration = pref.creneau.duration
        pref.save()
        


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_courseslot_generalslot_step'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseslot',
            name='generalslot_ptr',
        ),
        migrations.RemoveField(
            model_name='step',
            name='generalslot_ptr',
        ),
        migrations.AddField(
            model_name='coursepreference',
            name='day',
            field=models.CharField(choices=[('m', 'monday'), ('tu', 'tuesday'), ('w', 'wednesday'), ('th', 'thursday'), ('f', 'friday'), ('sa', 'saturday'), ('su', 'sunday')], default='m', max_length=2),
        ),
        migrations.AddField(
            model_name='coursepreference',
            name='duration',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coursepreference',
            name='start_time',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='roompreference',
            name='day',
            field=models.CharField(choices=[('m', 'monday'), ('tu', 'tuesday'), ('w', 'wednesday'), ('th', 'thursday'), ('f', 'friday'), ('sa', 'saturday'), ('su', 'sunday')], default='m', max_length=2),
        ),
        migrations.AddField(
            model_name='roompreference',
            name='duration',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='roompreference',
            name='start_time',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='day',
            field=models.CharField(choices=[('m', 'monday'), ('tu', 'tuesday'), ('w', 'wednesday'), ('th', 'thursday'), ('f', 'friday'), ('sa', 'saturday'), ('su', 'sunday')], default='m', max_length=2),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='duration',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='start_time',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='CourseSlot',
        ),
        migrations.DeleteModel(
            name='GeneralSlot',
        ),
        migrations.DeleteModel(
            name='Step',
        ),
        migrations.RunPython(translate_slot_preferences),
    ]
