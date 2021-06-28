# Generated by Django 3.1.7 on 2021-06-18 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0077_auto_20210511_1707'),
    ]

    operations = [
        migrations.RenameModel('Group', 'StructuralGroup'),
        migrations.AlterField(
            model_name='course',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='courses', to='base.StructuralGroup'),
        ),
    ]
