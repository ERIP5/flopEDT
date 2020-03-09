# Generated by Django 2.1.3 on 2020-03-09 18:26

from django.db import migrations

def room2roomgroup(apps, schema_editor):
    Room = apps.get_model('base', 'Room')
    RoomGroup = apps.get_model('base', 'RoomGroup')
    Department = apps.get_model('base', 'Department')

    room_groups = {}

    room_names = [r.name for r in Room.objects.all()]

    # New roomgroups for basic rooms
    for room in Room.objects.all():
        print(room)
        room_groups[room.name] = {}
        room_groups[room.name] = [rg.name for rg in room.subroom_of.all()]

        # Keep departments from Room and types from RoomGroup(s)
        associated_rg = RoomGroup.objects.filter(name=room.name)
        nb_rg = associated_rg.count()
        print(f'{nb_rg} associated roomgroup(s)')
        if nb_rg > 1:
            all_types = set()
            for rg in associated:
                all_types.update(rg.types.all())
            associated_rg.delete()
            associated_rg = RoomGroup(name=room.name)
            associated_rg.save()
            associated_rg.types.add(*list(all_types))
        elif nb_rg == 0:
            associated_rg = RoomGroup(name=room.name)
        else:
            associated_rg = associated_rg[0]
        associated_rg.basic = True
        associated_rg.save()
        associated_rg.departments.add(*room.departments.all())
        print(f'{associated_rg.basic} {associated_rg.types.all()} {associated_rg.departments.all()}')

    # associate roomgroups to newly created RoomGroup
    print("Subrooms")
    for room in Room.objects.all():
        associated_rg = RoomGroup.objects.get(name=room.name)
        is_in = [rg for rg in RoomGroup.objects.filter(name__in=room_groups[room.name]) if rg.name != room.name]
        associated_rg.subroom_of.add(*is_in)
        print(f'{associated_rg.name} {associated_rg.basic} {associated_rg.types.all()} {associated_rg.departments.all()}')

    print("Departments")
    # departments according to basic rooms
    for rg in RoomGroup.objects.all().exclude(name__in=room_names):
        depts = set(Department.objects.all())
        for room in rg.subrooms.all():
            depts &= set(room.departments.all())
        rg.departments.clear()
        rg.departments.add(*list(depts))
        print(f'{rg.name} {rg.basic} {rg.types.all()} {rg.departments.all()}')


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_auto_20200309_2255'),
    ]

    operations = [
        migrations.RunPython(room2roomgroup),
    ]
