# Generated by Django 3.0.14 on 2022-07-23 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0034_themespreferences'),
        ('TTapp', '0062_limitcoursetypetimeperperiod'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignallcourses',
            options={'verbose_name': 'Each course is assigned to one tutor (max)', 'verbose_name_plural': 'Each course is assigned to one tutor (max)'},
        ),
        migrations.AlterModelOptions(
            name='avoidbothtimes',
            options={'verbose_name': 'Avoid using both times', 'verbose_name_plural': 'Avoid using both times'},
        ),
        migrations.AlterModelOptions(
            name='boundphysicalpresencehalfdays',
            options={'verbose_name': 'Bound physical presence half days', 'verbose_name_plural': 'Bound physical presence half days'},
        ),
        migrations.AlterModelOptions(
            name='breakaroundcoursetype',
            options={'verbose_name': 'A break around some type courses', 'verbose_name_plural': 'A break around some type courses'},
        ),
        migrations.AlterModelOptions(
            name='considerdependencies',
            options={'verbose_name': 'Consider dependecies', 'verbose_name_plural': 'Consider dependecies'},
        ),
        migrations.AlterModelOptions(
            name='considerpivots',
            options={'verbose_name': 'Consider pivots', 'verbose_name_plural': 'Consider pivots'},
        ),
        migrations.AlterModelOptions(
            name='considerroomsorts',
            options={'verbose_name': 'Consider tutors rooms sorts', 'verbose_name_plural': 'Consider tutors rooms sorts'},
        ),
        migrations.AlterModelOptions(
            name='considertutorsunavailability',
            options={'verbose_name': "Consider tutors' unvailabilities", 'verbose_name_plural': "Consider tutors' unvailabilities"},
        ),
        migrations.AlterModelOptions(
            name='curfew',
            options={'verbose_name': 'Curfew', 'verbose_name_plural': 'Curfew'},
        ),
        migrations.AlterModelOptions(
            name='groupslunchbreak',
            options={'verbose_name': 'Lunch break for groups', 'verbose_name_plural': 'Lunch break for groups'},
        ),
        migrations.AlterModelOptions(
            name='limitedroomchoices',
            options={'verbose_name': 'Limited room choices', 'verbose_name_plural': 'Limited room choices'},
        ),
        migrations.AlterModelOptions(
            name='limitedstarttimechoices',
            options={'verbose_name': 'Limited start time choices', 'verbose_name_plural': 'Limited start time choices'},
        ),
        migrations.AlterModelOptions(
            name='limitgroupmoves',
            options={'verbose_name': 'Limit room moves for groups', 'verbose_name_plural': 'Limit room moves for groups'},
        ),
        migrations.AlterModelOptions(
            name='limitgroupsphysicalpresence',
            options={'verbose_name': 'Limit simultaneous physical presence', 'verbose_name_plural': 'Limit simultaneous physical presence'},
        ),
        migrations.AlterModelOptions(
            name='limitgroupstimeperperiod',
            options={'verbose_name': 'Limit groups busy time per period', 'verbose_name_plural': 'Limit groups busy time per period'},
        ),
        migrations.AlterModelOptions(
            name='limitholes',
            options={'verbose_name': 'Limit holes', 'verbose_name_plural': 'Limit holes'},
        ),
        migrations.AlterModelOptions(
            name='limitmodulestimeperperiod',
            options={'verbose_name': 'Limit modules busy time per period', 'verbose_name_plural': 'Limit modules busy time per period'},
        ),
        migrations.AlterModelOptions(
            name='limitsimultaneouscoursesnumber',
            options={'verbose_name': 'Limit simultaneous courses number', 'verbose_name_plural': 'Limit simultaneous courses number'},
        ),
        migrations.AlterModelOptions(
            name='limittutormoves',
            options={'verbose_name': 'Limit room moves for tutors', 'verbose_name_plural': 'Limit room moves for tutors'},
        ),
        migrations.AlterModelOptions(
            name='limittutorstimeperperiod',
            options={'verbose_name': 'Limit tutors busy time per period', 'verbose_name_plural': 'Limit tutors busy time per period'},
        ),
        migrations.AlterModelOptions(
            name='limittutortimeperweeks',
            options={'verbose_name': 'Limit time per weeks for tutors', 'verbose_name_plural': 'Limit time per weeks for tutors'},
        ),
        migrations.AlterModelOptions(
            name='limitundesiredslotsperweek',
            options={'verbose_name': 'Limit undesired slots per week', 'verbose_name_plural': 'Limit undesired slots per week'},
        ),
        migrations.AlterModelOptions(
            name='locateallcourses',
            options={'verbose_name': 'Assign a room to the courses', 'verbose_name_plural': 'Assign a room to the courses'},
        ),
        migrations.AlterModelOptions(
            name='lowerboundbusydays',
            options={'verbose_name': 'Lower bound tutor busy days', 'verbose_name_plural': 'Lower bound tutor busy days'},
        ),
        migrations.AlterModelOptions(
            name='mingroupshalfdays',
            options={'verbose_name': 'Minimize busy half-days for groups', 'verbose_name_plural': 'Minimize busy half-days for groups'},
        ),
        migrations.AlterModelOptions(
            name='minmoduleshalfdays',
            options={'verbose_name': 'Minimize used half-days for modules', 'verbose_name_plural': 'Minimize used half-days for modules'},
        ),
        migrations.AlterModelOptions(
            name='minnonpreferedtrainprogsslot',
            options={'verbose_name': 'Minimize undesired slots for groups', 'verbose_name_plural': 'Minimize undesired slots for groups'},
        ),
        migrations.AlterModelOptions(
            name='minnonpreferedtutorsslot',
            options={'verbose_name': 'Minimize undesired slots for tutors', 'verbose_name_plural': 'Minimize undesired slots for tutors'},
        ),
        migrations.AlterModelOptions(
            name='mintutorshalfdays',
            options={'verbose_name': 'Minimize busy half days for tutors', 'verbose_name_plural': 'Minimize busy half days for tutors'},
        ),
        migrations.AlterModelOptions(
            name='modulesbybloc',
            options={'verbose_name': 'Gather courses of considered modules', 'verbose_name_plural': 'Gather courses of considered modules'},
        ),
        migrations.AlterModelOptions(
            name='nogroupcourseonday',
            options={'verbose_name': 'No courses on declared days for groups', 'verbose_name_plural': 'No courses on declared days for groups'},
        ),
        migrations.AlterModelOptions(
            name='nosimultaneousgroupcourses',
            options={'verbose_name': 'No simultaneous courses for groups', 'verbose_name_plural': 'No simultaneous courses for groups'},
        ),
        migrations.AlterModelOptions(
            name='notutorcourseonday',
            options={'verbose_name': 'No courses on declared days for tutors', 'verbose_name_plural': 'No courses on declared days for tutors'},
        ),
        migrations.AlterModelOptions(
            name='novisio',
            options={'verbose_name': 'No visio courses', 'verbose_name_plural': 'No visio courses'},
        ),
        migrations.AlterModelOptions(
            name='respectmaxhoursperday',
            options={'verbose_name': 'Respect max hours per days bounds', 'verbose_name_plural': 'Respect max hours per days bounds'},
        ),
        migrations.AlterModelOptions(
            name='respectminhoursperday',
            options={'verbose_name': 'Respect min hours per day bounds', 'verbose_name_plural': 'Respect min hours per day bounds'},
        ),
        migrations.AlterModelOptions(
            name='scheduleallcourses',
            options={'verbose_name': 'Schedule once all considered courses', 'verbose_name_plural': 'Schedule once all considered courses'},
        ),
        migrations.AlterModelOptions(
            name='simultaneouscourses',
            options={'verbose_name': 'Simultaneous courses', 'verbose_name_plural': 'Simultaneous courses'},
        ),
        migrations.AlterModelOptions(
            name='stabilizationthroughweeks',
            options={'verbose_name': 'Stabilization through weeks', 'verbose_name_plural': 'Stabilization through weeks'},
        ),
        migrations.AlterModelOptions(
            name='stabilizegroupscourses',
            options={'verbose_name': 'Stabilize groups courses', 'verbose_name_plural': 'Stabilize groups courses'},
        ),
        migrations.AlterModelOptions(
            name='stabilizetutorscourses',
            options={'verbose_name': 'Stabilize tutors courses', 'verbose_name_plural': 'Stabilize tutors courses'},
        ),
        migrations.AlterModelOptions(
            name='tutorslunchbreak',
            options={'verbose_name': 'Lunch break for tutors', 'verbose_name_plural': 'Lunch break for tutors'},
        ),
        migrations.AlterModelOptions(
            name='visioonly',
            options={'verbose_name': 'Only visio courses', 'verbose_name_plural': 'Only visio courses'},
        ),
        migrations.AlterField(
            model_name='limitundesiredslotsperweek',
            name='tutors',
            field=models.ManyToManyField(blank=True, to='people.Tutor', verbose_name='Tutors'),
        ),
    ]
