# Generated by Django 3.0.5 on 2020-09-10 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0059_courseadditional'),
        ('people', '0017_notificationspreferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouppreferences',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to='base.Group'),
        ),
        migrations.AlterField(
            model_name='studentpreferences',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to='people.Student'),
        ),
    ]
