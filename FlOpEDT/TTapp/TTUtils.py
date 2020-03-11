# coding:utf-8

# !/usr/bin/python

# This file is part of the FlOpEDT/FlOpScheduler project.
# Copyright (c) 2017
# Authors: Iulian Ober, Paul Renaud-Goud, Pablo Seban, et al.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>.
#
# You can be released from the requirements of the license by purchasing
# a commercial license. Buying such a license is mandatory as soon as
# you develop activities involving the FlOpEDT/FlOpScheduler software
# without disclosing the source code of your own applications.

from base.models import ScheduledCourse, RoomPreference, EdtVersion, Department, CourseStartTimeConstraint,\
    TimeGeneralSettings, Room, CourseModification
from base.timing import str_slot
from django.db.models import Count, Max, Q, F
from TTapp.models import LimitedRoomChoices, slot_pause
from base.views import get_key_course_pl, get_key_course_pp
from django.core.cache import cache

def basic_reassign_rooms(department, week, year, target_work_copy):
    """
    Reassign the rooms to minimize moves...
    """
    print("reassigning rooms to minimize moves...")

    scheduled_courses_params = {
        'course__module__train_prog__department': department,
        'course__week': week,
        'course__year': year,
        'work_copy': target_work_copy,
    }

    possible_start_times = set()
    for c in CourseStartTimeConstraint.objects.filter(course_type__department=department):
        possible_start_times |= set(c.allowed_start_times)
    possible_start_times = list(possible_start_times)
    possible_start_times.sort()
    days = TimeGeneralSettings.objects.get(department=department).days

    for day in days:
        for st in possible_start_times:
            rank = possible_start_times.index(st)
            if rank == 0:
                continue
            nsl = ScheduledCourse.objects.filter(
                                            start_time=st, day=day,
                                            **scheduled_courses_params)
            # print sl
            for CP in nsl:
                precedent = ScheduledCourse \
                    .objects \
                    .filter(start_time__lte=st - F('course__type__duration'),
                            start_time__gt=st - F('course__type__duration') - slot_pause,
                            day=day,
                            course__room_type=CP.course.room_type,
                            course__tutor=CP.course.tutor,
                            **scheduled_courses_params)
                if len(precedent) == 0:
                    precedent = ScheduledCourse \
                        .objects \
                        .filter(start_time__lte = st - F('course__type__duration'),
                                start_time__gt = st - F('course__type__duration') - slot_pause,
                                day=day,
                                course__room_type=CP.course.room_type,
                                course__group=CP.course.group,
                                **scheduled_courses_params)
                    if len(precedent) == 0:
                        continue
                precedent = precedent[0]
                # print "### has prec, trying to reassign:", precedent, "\n\t",
                cp_using_prec = ScheduledCourse \
                    .objects \
                    .filter(start_time=st,
                            day=day,
                            room=precedent.room,
                            **scheduled_courses_params)
                # test if lucky
                if cp_using_prec.count() == 1 and cp_using_prec[0] == CP:
                    # print "lucky, no change needed"
                    continue
                # test if precedent.room is available
                prec_is_unavailable = False
                for r in precedent.room.and_subrooms():
                    if RoomPreference.objects.filter(week=week, year=year,  day=day,
                                                     start_time=st, room=r, value=0).exists():
                        prec_is_unavailable = True

                    if ScheduledCourse.objects \
                        .filter(start_time=st,
                                day=day,
                                room__in={r}|set(r.subroom_of.exclude(id=precedent.room.id)),
                                **scheduled_courses_params) \
                        .exists():
                            prec_is_unavailable = True

                if prec_is_unavailable:
                    # print "room is not available"
                    continue

                # test if precedent.room is used for course of the same room_type and swap
                if not cp_using_prec.exists():
                    CP.room = precedent.room
                    CP.save()
                    # print "assigned", CP
                elif cp_using_prec.count() == 1:
                    sib = cp_using_prec[0]
                    if sib.course.room_type == CP.course.room_type and sib.course:
                        if not LimitedRoomChoices.objects.filter(
                                    Q(week=week) | Q(week=None),
                                    Q(year=year) | Q(year=None),
                                    Q(train_prog=sib.course.module.train_prog) | Q(module=sib.course.module) | Q(group=sib.course.group) |
                                    Q(tutor=sib.course.tutor) | Q(type=sib.course.type),
                                    possible_rooms=sib.room).exists():
                            r = CP.room
                            CP.room = precedent.room
                            sib.room = r
                            CP.save()
                            sib.save()
                        # print "swapped", CP, " with", sib
    cache.delete(get_key_course_pl(department.abbrev,
                                   year,
                                   week,
                                   target_work_copy))
    print("done")


def get_shared_tutors(department, week, year, copy_a):
    '''
    Returns tutors that are busy both in the department for the given week (work_copy copy_a)
    and in another department (work_copy 0)
    '''
    busy_tutors_in_dept = [s.tutor for s in ScheduledCourse\
                      .objects\
                      .select_related('course__module__train_prog__department',
                                      'tutor')\
                      .filter(course__module__train_prog__department__abbrev=department,
                              course__week=week,
                              course__year=year,
                              work_copy=copy_a)\
                      .distinct('tutor')]
    return [s.tutor.username for s in ScheduledCourse\
            .objects\
            .select_related('course__module__train_prog__department')\
            .exclude(course__module__train_prog__department__abbrev=department)\
            .filter(course__week=week,
                    course__year=year,
                    tutor__in=busy_tutors_in_dept,
                    work_copy=0)\
            .distinct('tutor')]


def get_shared_rooms():
    '''
    Returns the rooms that are shared between departments
    '''
    return Room.objects.annotate(num_depts=Count('departments')).filter(num_depts__gt=1)


def compute_conflicts_helper(dic):
    '''
    Computes overlapping slots
    '''
    conflicts = []
    for k in dic:
        dic[k].sort(key=lambda s: (s['day'], s['start_time']))
    for t, sched_list in dic.items():
        for i in range(len(sched_list)-1):
            if sched_list[i]['day'] == sched_list[i+1]['day'] and\
               sched_list[i]['start_time'] + sched_list[i]['duration'] > sched_list[i+1]['start_time']:
                conflicts.append((sched_list[i],sched_list[i+1]))
    return conflicts
    

def compute_conflicts(department, week, year, copy_a):
    '''
    Computes the conflicts (tutor giving several courses at the same time or
    room used in parallel) in week (year,week) between the work copy copy_a
    of department department, and work copy 0 of the other departments.
    '''
    conflicts = {}

    # tutors with overlapping courses
    dic_by_tutor = {}
    tmp_conflicts = []
    tutors_username_list = get_shared_tutors(department, week, year, copy_a)
    courses_list = ScheduledCourse.objects.select_related('course__module__train_prog__department',
                                                          'course__type__duration',
                                                          'tutor')\
                                          .filter(Q(work_copy=copy_a) & Q(course__module__train_prog__department__abbrev=department) \
                                                  | Q(work_copy=0)&~Q(course__module__train_prog__department__abbrev=department),
                                                  course__week=week,
                                                  course__year=year,
                                                  tutor__username__in=tutors_username_list,
                                          )\
                                          .annotate(duration=F('course__type__duration'),
                                                    week=F('course__week'),
                                                    year=F('course__year'))\
                                          .values('id',
                                                  'year', 'week',
                                                  'day','start_time','duration','tutor__username')
    for t in tutors_username_list:
        dic_by_tutor[t] = []
    for sc in courses_list:
        dic_by_tutor[sc['tutor__username']].append(sc)
    conflicts['tutor'] = compute_conflicts_helper(dic_by_tutor)

    # rooms that are used in parallel
    tmp_conflicts = []
    dic_by_room = {}
    dic_subrooms = {}
    conflict_room_list = get_shared_rooms()
    
    for room in conflict_room_list:
        dic_subrooms[str(room.id)] = [r.name for r in room.and_subrooms()]
    print(dic_subrooms)
    courses_list = ScheduledCourse.objects.select_related('course__type__duration')\
                                          .filter(Q(work_copy=copy_a) & Q(course__module__train_prog__department__abbrev=department) \
                                                  | Q(work_copy=0)&~Q(course__module__train_prog__department__abbrev=department),
                                                  course__week=week,
                                                  course__year=year,
                                                  work_copy=copy_a,
                                                  room__in=conflict_room_list)\
                                          .annotate(duration=F('course__type__duration'),
                                                    week=F('course__week'),
                                                    year=F('course__year'))\
                                          .values('id',
                                                  'year', 'week',
                                                  'day','start_time','duration','room')
    for room in get_shared_rooms():
        dic_by_room[room.name] = []

    # create busy slots for every room in the roomgroups
    for sc in courses_list:
        roomgroup = sc['room']
        for subroom in dic_subrooms[str(roomgroup)]:
            if subroom in dic_by_room:
                new_sc = sc.copy()
                new_sc['room'] = subroom
                dic_by_room[new_sc['room']].append(new_sc)

    conflicts['room'] = compute_conflicts_helper(dic_by_room)

    return conflicts


def get_conflicts(department, week, year, copy_a):
    '''
    Checks whether the work copy copy_a of department department is compatible
    with the work copies 0 of the other departments.
    Returns a result {'status':'blabla', 'more':'explanation'}
    '''
    result = {'status':'OK'}
    more = ''
    
    conflicts = compute_conflicts(department, week, year, copy_a)

    if len(conflicts['tutor']) + len(conflicts['room']) == 0:
        return result
    
    if len(conflicts['tutor']) > 0:
        more += 'Prof déjà occupé·e : '
        for conflict in conflicts['tutor']:
            sched = []
            for sc in conflict:
                sched.append(ScheduledCourse.objects.get(id=sc['id']))
            more += sc['tutor__username'] + ' : '
            str_sched = list(map(
                lambda s: f'{str_slot(s.day,s.start_time,s.course.type.duration)} '\
                + f'({s.course.module.abbrev}, {s.course.module.train_prog.department.abbrev})',
                sched))
            more += ' VS '.join(str_sched) + ' ; '

    if len(conflicts['room']) > 0:
        more += 'Salle déjà prise : '
        for conflict in conflicts['room']:
            sched = []
            for sc in conflict:
                sched.append(ScheduledCourse.objects.get(id=sc['id']))
            str_sched = list(map(
                lambda s: f'{s.room} ({str_slot(s.day,s.start_time,s.course.type.duration)}, '\
                + f'{s.tutor.username}, {s.course.module.train_prog.department.abbrev})',
                sched))
            more += ' VS '.join(str_sched) + ' ; '

    result['status'] = 'KO'
    result['more'] = more

    return result


def basic_swap_version(department, week, year, copy_a, copy_b=0):

    scheduled_courses_params = {
        'course__module__train_prog__department': department,
        'course__week': week,
        'course__year': year,
    }

    try:
        tmp_wc = ScheduledCourse \
                     .objects \
                     .filter(**scheduled_courses_params) \
                     .aggregate(Max('work_copy'))['work_copy__max'] + 1
    except KeyError:
        print('No scheduled courses')
        return

    version_copy = EdtVersion.objects.get(department=department, week=week, year=year)

    for cp in ScheduledCourse.objects.filter(work_copy=copy_a, **scheduled_courses_params):
        cp.work_copy = tmp_wc
        cp.save()

    for cp in ScheduledCourse.objects.filter(work_copy=copy_b, **scheduled_courses_params):
        cp.work_copy = copy_a
        cp.save()

    for cp in ScheduledCourse.objects.filter(work_copy=tmp_wc, **scheduled_courses_params):
        cp.work_copy = copy_b
        cp.save()

    if copy_a == 0 or copy_b == 0:
        CourseModification.objects.filter(course__year=year,
                                          course__week=week).delete()
        version_copy.version += 1
        version_copy.save()

    cache.delete(get_key_course_pl(department.abbrev,
                                   year,
                                   week,
                                   copy_a))
    cache.delete(get_key_course_pl(department.abbrev,
                                   year,
                                   week,
                                   copy_b))
    cache.delete(get_key_course_pp(department.abbrev,
                                   year,
                                   week,
                                   copy_a))
    cache.delete(get_key_course_pp(department.abbrev,
                                   year,
                                   week,
                                   copy_b))
