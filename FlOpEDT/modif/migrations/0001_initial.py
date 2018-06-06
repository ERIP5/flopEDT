# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-06 10:25
from __future__ import unicode_literals

import caching.base
import colorfield.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BIATOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BreakingNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('year', models.PositiveSmallIntegerField()),
                ('x_beg', models.FloatField(blank=True, default=2.0)),
                ('x_end', models.FloatField(blank=True, default=3.0)),
                ('y', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('txt', models.CharField(max_length=200)),
                ('is_linked', models.URLField(blank=True, default=None, null=True)),
                ('fill_color', colorfield.fields.ColorField(default='#228B22', max_length=18)),
                ('strk_color', colorfield.fields.ColorField(default='#000000', max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('semaine', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('suspens', models.BooleanField(default=False, verbose_name='En suspens?')),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CourseModification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine_old', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an_old', models.PositiveSmallIntegerField(null=True)),
                ('version_old', models.PositiveIntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Course')),
            ],
        ),
        migrations.CreateModel(
            name='CoursePreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField(null=True)),
                ('valeur', models.SmallIntegerField(default=8, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)])),
            ],
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('no', models.PositiveSmallIntegerField(primary_key=True, serialize=False, verbose_name='Number')),
                ('nom', models.CharField(max_length=10, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('successifs', models.BooleanField(default=False, verbose_name='Successifs?')),
                ('ND', models.BooleanField(default=False, verbose_name='Jours differents')),
                ('cours1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cours1', to='modif.Course')),
                ('cours2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cours2', to='modif.Course')),
            ],
        ),
        migrations.CreateModel(
            name='EdtVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('version', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FullStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(default='INFO', max_length=50)),
                ('is_iut', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=4)),
                ('size', models.PositiveSmallIntegerField()),
                ('basic', models.BooleanField(default=False, verbose_name='Basic group?')),
                ('parent_groups', models.ManyToManyField(blank=True, related_name='_group_parent_groups_+', to='modif.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('valeur', models.FloatField()),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_height', models.PositiveIntegerField(default=None, null=True)),
                ('button_txt', models.CharField(default=None, max_length=20, null=True)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='display', to='modif.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupFreeHalfDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('DJL', models.PositiveSmallIntegerField()),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apm', models.CharField(blank=True, choices=[('AM', 'AM'), ('PM', 'PM')], default=None, max_length=2, null=True, verbose_name='Demi-journ\xe9e')),
                ('week', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('year', models.PositiveSmallIntegerField()),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Day')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, null=True)),
                ('abbrev', models.CharField(max_length=10, verbose_name='Intitul\xe9 abbr\xe9g\xe9')),
                ('ppn', models.CharField(default='M', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_bg', models.CharField(default='red', max_length=20)),
                ('color_txt', models.CharField(default='black', max_length=20)),
                ('module', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='display', to='modif.Module')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('starting_week', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('ending_week', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
            ],
        ),
        migrations.CreateModel(
            name='PlanningModification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine_old', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an_old', models.PositiveSmallIntegerField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Regen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('full', models.BooleanField(default=True, verbose_name='Compl\xe8te')),
                ('fday', models.PositiveSmallIntegerField(default=1, verbose_name='Jour')),
                ('fmonth', models.PositiveSmallIntegerField(default=1, verbose_name='Mois')),
                ('fyear', models.PositiveSmallIntegerField(default=1, verbose_name='Ann\xe9e')),
                ('stabilize', models.BooleanField(default=False, verbose_name='Stabilis\xe9e')),
                ('sday', models.PositiveSmallIntegerField(default=1, verbose_name='Jour')),
                ('smonth', models.PositiveSmallIntegerField(default=1, verbose_name='Mois')),
                ('syear', models.PositiveSmallIntegerField(default=1, verbose_name='Ann\xe9e')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RoomGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RoomPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField(null=True)),
                ('valeur', models.SmallIntegerField(default=8, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)])),
            ],
        ),
        migrations.CreateModel(
            name='RoomSort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ScheduledCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('noprec', models.BooleanField(default=True, verbose_name='vrai si on ne veut pas garder la salle')),
                ('copie_travail', models.PositiveSmallIntegerField(default=0)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Course')),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveSmallIntegerField(default=90, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(240)])),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SupplyStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer', models.CharField(max_length=50, null=True, verbose_name='Employeur ?')),
                ('qualite', models.CharField(max_length=50, null=True)),
                ('field', models.CharField(max_length=50, null=True, verbose_name='Domaine ?')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('apm', models.CharField(choices=[('AM', 'AM'), ('PM', 'PM')], default='AM', max_length=2, verbose_name='Half day')),
                ('no', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingHalfDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apm', models.CharField(blank=True, choices=[('AM', 'AM'), ('PM', 'PM')], default=None, max_length=2, null=True, verbose_name='Demi-journ\xe9e')),
                ('week', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('year', models.PositiveSmallIntegerField()),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Day')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingProgramme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('abbrev', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingProgrammeDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveSmallIntegerField()),
                ('training_programme', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='display', to='modif.TrainingProgramme')),
            ],
        ),
        migrations.CreateModel(
            name='TutorCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('valeur', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField(null=True)),
                ('valeur', models.SmallIntegerField(default=8, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)])),
                ('creneau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Slot')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('modif.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('pref_slots_per_day', models.PositiveSmallIntegerField(default=4, verbose_name='How many slots per day would you prefer ?')),
                ('rights', models.PositiveSmallIntegerField(default=0, verbose_name='Peut forcer ?')),
                ('LBD', models.PositiveSmallIntegerField(default=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)], verbose_name='Limitation du nombre de jours')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('modif.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='userpreference',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='traininghalfday',
            name='train_prog',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='modif.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='slot',
            name='heure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Time'),
        ),
        migrations.AddField(
            model_name='slot',
            name='jour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Day'),
        ),
        migrations.AddField(
            model_name='scheduledcourse',
            name='creneau',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Slot'),
        ),
        migrations.AddField(
            model_name='scheduledcourse',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modif.RoomGroup'),
        ),
        migrations.AddField(
            model_name='roomsort',
            name='for_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='modif.RoomType'),
        ),
        migrations.AddField(
            model_name='roomsort',
            name='prefer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='modif.RoomGroup'),
        ),
        migrations.AddField(
            model_name='roomsort',
            name='unprefer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='modif.RoomGroup'),
        ),
        migrations.AddField(
            model_name='roompreference',
            name='creneau',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Slot'),
        ),
        migrations.AddField(
            model_name='roompreference',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Room'),
        ),
        migrations.AddField(
            model_name='roomgroup',
            name='types',
            field=models.ManyToManyField(blank=True, related_name='members', to='modif.RoomType'),
        ),
        migrations.AddField(
            model_name='room',
            name='subroom_of',
            field=models.ManyToManyField(blank=True, related_name='subrooms', to='modif.RoomGroup'),
        ),
        migrations.AddField(
            model_name='module',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Period'),
        ),
        migrations.AddField(
            model_name='module',
            name='train_prog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='group',
            name='train_prog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='group',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.GroupType'),
        ),
        migrations.AddField(
            model_name='coursepreference',
            name='course_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.CourseType'),
        ),
        migrations.AddField(
            model_name='coursepreference',
            name='creneau',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Slot'),
        ),
        migrations.AddField(
            model_name='coursepreference',
            name='train_prog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='coursemodification',
            name='creneau_old',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modif.Slot'),
        ),
        migrations.AddField(
            model_name='coursemodification',
            name='room_old',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modif.RoomGroup'),
        ),
        migrations.AddField(
            model_name='course',
            name='groupe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Group'),
        ),
        migrations.AddField(
            model_name='course',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module', to='modif.Module'),
        ),
        migrations.AddField(
            model_name='course',
            name='modulesupp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulesupp', to='modif.Module'),
        ),
        migrations.AddField(
            model_name='course',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modif.RoomType'),
        ),
        migrations.AddField(
            model_name='course',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.CourseType'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='tutorcost',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Tutor'),
        ),
        migrations.AddField(
            model_name='supplystaff',
            name='tutor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='modif.Tutor'),
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Group'),
        ),
        migrations.AddField(
            model_name='planningmodification',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operated_planif_modif', to='modif.Tutor'),
        ),
        migrations.AddField(
            model_name='planningmodification',
            name='tutor_old',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='impacted_by_planif_modif', to='modif.Tutor'),
        ),
        migrations.AddField(
            model_name='module',
            name='head',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='modif.Tutor'),
        ),
        migrations.AddField(
            model_name='fullstaff',
            name='tutor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='modif.Tutor'),
        ),
        migrations.AddField(
            model_name='coursemodification',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Tutor'),
        ),
        migrations.AddField(
            model_name='course',
            name='supp_tutor',
            field=models.ManyToManyField(blank=True, related_name='courses_as_supp', to='modif.Tutor'),
        ),
        migrations.AddField(
            model_name='course',
            name='tutor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taught_courses', to='modif.Tutor'),
        ),
        migrations.AddField(
            model_name='biatos',
            name='tutor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='modif.Tutor'),
        ),
    ]
