# coding: utf8
# -*- coding: utf-8 -*-

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

import logging

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from base.models import Group, TrainingProgramme, \
                        ScheduledCourse, EdtVersion, Department, Regen

from base.models import Room, RoomType, RoomGroup, \
                        RoomSort, Period, CourseType, \
                        TutorCost, CourseStartTimeConstraint, \
                        TimeGeneralSettings, GroupType

from displayweb.models import GroupDisplay, TrainingProgrammeDisplay, BreakingNews

from people.models import Tutor
from TTapp.models import TTConstraint

logger = logging.getLogger(__name__)


@transaction.atomic
def create_first_department():    

    department = Department.objects.create(name="Default Department", abbrev="default")
    
    # Update all existing department related models
    models = [
        TrainingProgramme, EdtVersion, Regen, \
        RoomType, Period, CourseType, BreakingNews, \
        TutorCost, GroupType]
   
    for model in models:
        model.objects.all().update(department=department)

    # Update all ManyToMany relations with Department
    models = [Tutor]
    for model in models:
        for model_class in model.objects.all():
            model_class.departments.add(department)

    # Update existing Constraint
    types = TTConstraint.__subclasses__()

    for type in types:
        type.objects.all().update(department=department)    

    # Init TimeGeneralSettings with default values
    TimeGeneralSettings.objects.create(
                        department=department,
                        day_start_time=8*60,
                        day_finish_time=18*60+45,
                        lunch_break_start_time=12*60+30,
                        lunch_break_finish_time=14*60,
                        days=["m", "tu", "w", "th", "f"])

    return department


def get_edt_version(department, week, year, create=False):

    params = {'semaine': week, 'an': year, 'department': department}

    if create:
        try:
            edt_version, _ = EdtVersion.objects.get_or_create(defaults={'version': 0}, **params)
        except EdtVersion.MultipleObjectsReturned as e:
            logger.error(f'get_edt_version: database inconsistency, multiple objects returned for {params}')
            raise(e)
        else:    
            version = edt_version.version
    else:
        """
        Raise model.DoesNotExist to simulate get behaviour 
        when no item is matching filter parameters
        """
        try:
            version = EdtVersion.objects.filter(**params).values_list("version", flat=True)[0]   
        except IndexError:
            raise(EdtVersion.DoesNotExist)
    return version


def get_scheduled_courses(department, week, year, num_copy):

    qs = ScheduledCourse.objects \
                    .filter(
                        cours__module__train_prog__department=department,
                        cours__semaine=week,
                        cours__an=year,
                        copie_travail=num_copy)
    return qs    


def get_groups(department_abbrev):
    """
    Return the groups hierachical representation from database
    """
    final_groups = []

    # Filter TrainingProgramme by department
    training_program_query = TrainingProgramme.objects.filter(department__abbrev=department_abbrev)

    for train_prog in training_program_query:

        gp_dict_children = {}
        gp_master = None
        for gp in Group.objects.filter(train_prog=train_prog):
            if gp.full_name() in gp_dict_children:
                raise Exception('Group name should be unique')
            if gp.parent_groups.all().count() == 0:
                if gp_master is not None:
                    raise Exception('One single group is able to be without '
                                    'parents')
                gp_master = gp
            elif gp.parent_groups.all().count() > 1:
                raise Exception('Not tree-like group structures are not yet '
                                'handled')
            gp_dict_children[gp.full_name()] = []

        for gp in Group.objects.filter(train_prog=train_prog):
            for new_gp in gp.parent_groups.all():
                gp_dict_children[new_gp.full_name()].append(gp)

        final_groups.append(get_descendant_groups(gp_master, gp_dict_children))

    return final_groups


def get_descendant_groups(gp, children):
    """
    Gather informations about all descendants of a group gp
    :param gp:
    :param children: dictionary <group_full_name, list_of_children>
    :return: an object containing the informations on gp and its descendants
    """
    current = {}
    if not gp.parent_groups.all().exists():
        current['parent'] = 'null'
        tp = gp.train_prog
        current['promo'] = tp.abbrev
        try:
            tpd = TrainingProgrammeDisplay.objects.get(training_programme=tp)
            if tpd.short_name != '':
                current['promotxt'] = tpd.short_name
            else:
                current['promotxt'] = tp.abbrev
            current['row'] = tpd.row
        except ObjectDoesNotExist:
            raise Exception('You should indicate on which row a training '
                            'programme will be displayed '
                            '(cf TrainingProgrammeDisplay)')
    current['name'] = gp.nom
    try:
        gpd = GroupDisplay.objects.get(group=gp)
        if gpd.button_height is not None:
            current['buth'] = gpd.button_height
        if gpd.button_txt is not None:
            current['buttxt'] = gpd.button_txt
    except ObjectDoesNotExist:
        pass

    if len(children[gp.full_name()]) > 0:
        current['children'] = []
        for gp_child in children[gp.full_name()]:
            gp_obj = get_descendant_groups(gp_child, children)
            gp_obj['parent'] = gp.nom
            current['children'].append(gp_obj)

    return current


def get_rooms(department_abbrev):
    """
    From the data stored in the database, fill the room description file, that
    will be used by the website.
    All room that belongs to a roomgroup that belongs to at least one room type
    of department_abbrev
    :return: an object containing one dictionary roomtype -> (list of roomgroups),
    and one dictionary roomgroup -> (list of rooms)
    """
    dic_rt = {}
    dept_rg = set()

    for rt in RoomType.objects.filter(department__abbrev=department_abbrev):
        dic_rt[str(rt)] = []
        for rg in rt.members.all():
            dept_rg.add(rg)
            if str(rg) not in dic_rt[str(rt)]:
                dic_rt[str(rt)].append(str(rg))

    dic_rg = {}
    for rg in dept_rg:
        dic_rg[rg.name] = []
        for r in rg.subrooms.all():
            dic_rg[rg.name].append(str(r))

    return {'roomtypes':dic_rt,
            'roomgroups':dic_rg}


def get_coursetype_constraints(department_abbrev):
    """
    From the data stored in the database, fill the course type 
    description file (duration and allowed start times), that will
    be used by the website
    :return: a dictionary course type -> (object containing duration
    and list of allowed start times)
    """
    dic = {}
    for ct in CourseType.objects.filter(department__abbrev=department_abbrev):
        dic[ct.name] = {'duration':ct.duration,
                        'allowed_st':[]}
        for ct_constraint in \
              CourseStartTimeConstraint.objects.filter(course_type=ct):
            dic[ct.name]['allowed_st'] += ct_constraint.allowed_start_times
        if len(dic[ct.name]['allowed_st']) == 0:
            dic[ct.name]['allowed_st'] += \
                CourseStartTimeConstraint.objects.get(course_type=None).allowed_start_times
    return dic


def get_time_settings(dept):
    """
    :return: time general settings
    """
    ts = TimeGeneralSettings.objects.get(department=dept)
    time_settings = {'time':
                     {'day_start_time': ts.day_start_time,
                      'day_finish_time': ts.day_finish_time,
                      'lunch_break_start_time': ts.lunch_break_start_time,
                      'lunch_break_finish_time': ts.lunch_break_finish_time},
                     'days': ts.days}
    return time_settings


def get_departments():
    """
    :return: list of department abbreviations
    """
    return [d.abbrev for d in Department.objects.all()]
