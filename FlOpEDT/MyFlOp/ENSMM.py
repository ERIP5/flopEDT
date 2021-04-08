from base.models import Course, TrainingProgramme, Group, Department, \
    TimeGeneralSettings, CourseType, RoomType, CourseStartTimeConstraint
from people.models import Tutor
from people.tutor import fill_default_user_preferences
from configuration.deploy_database import extract_database_file
from MyFlOp.database_ENSMM import database_ENSMM
from MyFlOp.cours_ENSMM import cours_ENSMM
from configuration.hyperplanning import extract_courses_from_book
from misc.assign_colors import assign_module_color


def global_extraction(abbrev='ENSMM', name='ENSMM', delete_groups=True):
    extract_database_file(abbrev, name, book=database_ENSMM)
    dep = Department.objects.get(abbrev=abbrev)
    optimize_settings(dep)
    for t in Tutor.objects.filter(departments=dep):
        fill_default_user_preferences(t, dep)
    extract_courses_from_book(cours_ENSMM, dep, assign_colors=False)
    C = Course.objects.filter(type__department=dep)
    for c in C:
        c.year += 1
        c.save()
    apply_group_architecture(find_group_architecture(dep))
    if delete_groups:
        remove_slash_groups(dep)
        g, tp = useless_groups_and_train_progs(dep)
        delete_useless_groups(g, tp)
    assign_module_color(dep, overwrite=True)


def find_group_architecture(dep):
    result = {}
    for tp in TrainingProgramme.objects.filter(department=dep):
        result[tp.name]={}
        G = Group.objects.filter(train_prog=tp)
        for g in G:
            result[tp.name][g.name] = set()
            for g2 in G.exclude(id=g.id):
                if g2.name.startswith(g.name):
                    result[tp.name][g.name].add(g2.name)
            if not result[tp.name][g.name]:
                result[tp.name].pop(g.name)
        if not result[tp.name]:
            result.pop(tp.name)
    return result


def apply_group_architecture(group_architecture_dict):
    d = group_architecture_dict
    for tp in d:
        tpg = Group.objects.get(train_prog__name=tp, name=tp)
        for g in d[tp]:
            G = Group.objects.get(train_prog__name=tp, name=g)
            for g2 in d[tp][g]:
                G2 = Group.objects.get(train_prog__name=tp, name=g2)
                for pg in G2.parent_groups.all():
                    G2.parent_groups.remove(pg)
                G2.parent_groups.add(G)


def useless_groups_and_train_progs(dep):
    groups = set()
    train_progs = set()
    G = Group.objects.filter(train_prog__department=dep)
    C = Course.objects.filter(type__department=dep)
    for g in G:
        cg = C.filter(groups__in={g} | g.descendants_groups())
        if not cg:
            groups.add(g)
    for tp in TrainingProgramme.objects.filter(department=dep):
        if all(g in groups for g in G.filter(train_prog=tp)):
            train_progs.add(tp)
    return groups, train_progs


def delete_useless_groups(useless_groups, useless_train_progs):
    for g in useless_groups:
        g.delete()
    for tp in useless_train_progs:
        tp.delete()


def remove_slash_groups(dep):
    slash_groups = Group.objects.filter(name__contains='/', train_prog__department=dep)
    for g in slash_groups:
        names = g.name.split('/')
        groups = Group.objects.filter(name__in=names)
        for c in Course.objects.filter(groups=g):
            c.groups.remove(g)
            for group in groups:
                c.groups.add(group)
        g.train_prog.delete()


def optimize_settings(dep):
    tgs = TimeGeneralSettings.objects.get(department=dep)
    tgs.days = ['m', 'tu', 'w', 'th', 'f']
    tgs.default_preference_duration = 120
    tgs.save()
    CST = CourseStartTimeConstraint.objects.filter(course_type__department=dep)
    for cst in CST:
        l = [st for st in cst.allowed_start_times if st % 30 == 0]
        if l:
            cst.allowed_start_times = l
            cst.save()
    RT, created = RoomType.objects.get_or_create(name='None', department=dep)
    if created:
        C = Course.objects.filter(type__department=dep)
        for i, c in enumerate(C):
            if i % 10 != 0:
                c.room_type = RT
                c.save()

