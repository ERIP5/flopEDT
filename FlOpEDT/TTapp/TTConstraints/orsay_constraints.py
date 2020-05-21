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


from django.contrib.postgres.fields import ArrayField

from django.db import models

from django.core.exceptions import ObjectDoesNotExist

from base.timing import french_format
from base.timing import Day

from TTapp.ilp_constraints.constraint_type import ConstraintType
from TTapp.ilp_constraints.constraint import Constraint
from TTapp.slots import days_filter, slots_filter
from TTapp.TTConstraint import TTConstraint
from TTapp.TTConstraints.groups_constraints import considered_basic_groups
from TTapp.slots import Slot


class GroupsLunchBreak(TTConstraint):
    """
    Ensures time for lunch in a given interval for given groups (all if groups is Null)
    """

    start_time = models.PositiveSmallIntegerField()
    end_time = models.PositiveSmallIntegerField()
    weekdays = ArrayField(models.CharField(max_length=2, choices=Day.CHOICES), blank=True, null=True)
    lunch_length = models.PositiveSmallIntegerField()
    groups = models.ManyToManyField('base.Group', blank=True, related_name='lunch_breaks_constraints')

    def enrich_model(self, ttmodel, week, ponderation=100):
        considered_groups = considered_basic_groups(self, ttmodel)
        days = days_filter(ttmodel.wdb.days, week=week)
        try:
            days = days_filter(days, day_in=self.weekdays)
        except ObjectDoesNotExist:
            pass
        for day in days:
            local_slots = [Slot(day=day, start_time=st, end_time=st+self.lunch_length)
                           for st in range(self.start_time, self.end_time - self.lunch_length + 1, 15)]
            slots_nb = len(local_slots)
            # pour chaque groupe, au moins un de ces slots ne voit aucun cours lui être simultané
            slot_vars = {}

            for group in considered_groups:
                considered_courses = self.get_courses_queryset_by_parameters(ttmodel, week, group=group)
                for local_slot in local_slots:
                    # Je veux que slot_vars[group, local_slot] soit à 1
                    # si et seulement si undesired_scheduled_courses vaut plus que 1
                    undesired_scheduled_courses = \
                        ttmodel.sum(ttmodel.TT[sl, c] for c in considered_courses
                                    for sl in slots_filter(ttmodel.wdb.compatible_slots[c],
                                                           simultaneous_to=local_slot))
                    slot_vars[group, local_slot] = ttmodel.add_floor(name='',
                                                                     expr=undesired_scheduled_courses,
                                                                     floor=1,
                                                                     bound=len(considered_courses))
                not_ok = ttmodel.add_floor(name='',
                                           expr=ttmodel.sum(slot_vars[group, sl] for sl in local_slots),
                                           floor=slots_nb,
                                           bound=2 * slots_nb)
                if self.weight is None:
                    ttmodel.add_constraint(not_ok,'==', 0, Constraint())
                    # ttmodel.add_constraint(ttmodel.sum(slot_vars[group, sl] for sl in local_slots),
                    #                        '<=', len(local_slots),
                    #                        Constraint(constraint_type=ConstraintType.LUNCH_BREAK,
                    #                                   groups=group, days=day))
                else:
                    cost = not_ok * ponderation * self.local_weight()
                    # cost = ttmodel.sum(slot_vars[group, sl] for sl in local_slots) * ponderation \
                    #        * self.local_weight()
                    ttmodel.add_to_group_cost(group, cost, week)


    def one_line_description(self):
        text = f"Il faut une pause déjeuner d'au moins {self.lunch_length} minutes " \
               f"entre {french_format(self.start_time)} et {french_format(self.end_time)}"
        try:
            text += " les " + ', '.join([wd for wd in self.weekdays])
        except ObjectDoesNotExist:
            pass
        if self.groups.exists():
            text += ' pour les groupes ' + ', '.join([group.name for group in self.groups.all()])
        else:
            text += " pour tous les groupes"

        if self.train_progs.exists():
            text += ' de ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])
        else:
            text += " de toutes les promos."
        return text


class BreakAroundCourseType(TTConstraint):
    """
    Ensures that the courses of a given course type and other types of courses cannot be consecutive for the given groups.
    """
    weekdays = ArrayField(models.CharField(max_length=2, choices=Day.CHOICES), blank=True, null=True)
    groups = models.ManyToManyField('base.Group', blank=True, related_name='amphi_break_constraint')
    course_type = models.ForeignKey('base.CourseType', related_name='amphi_break_constraint', on_delete=models.CASCADE)

    def enrich_model(self, ttmodel, week, ponderation=1):
        considered_groups = considered_basic_groups(self, ttmodel)
        days = days_filter(ttmodel.wdb.days, week=week)
        try:
            days = days_filter(days, day_in=self.weekdays)
        except ObjectDoesNotExist:
            pass
        for group in considered_groups:
            amphis = set(self.get_courses_queryset_by_parameters(ttmodel, week, group=group, course_type=self.course_type))
            other_courses = set(self.get_courses_queryset_by_parameters(ttmodel, week, group=group).exclude(course_type=self.course_type))
            broken_breaks = ttmodel.lin_expr()
            for day in days:
                day_slots = slots_filter(ttmodel.wdb.courses_slots, day=day)
                for slot1 in day_slots:
                    successive_slots = slots_filter(day_slots, start_time=slot1.end_time)
                    if not successive_slots:
                        continue
                    amphi_slot1 = ttmodel.sum(ttmodel.TT[slot1, c] for c in amphis & ttmodel.wdb.compatible_courses[slot1])
                    other_slot1 = ttmodel.sum(ttmodel.TT[slot1, c] for c in other_courses & ttmodel.wdb.compatible_courses[slot1])
                    other_slot2 = ttmodel.sum(ttmodel.TT[slot2, c]
                                              for slot2 in successive_slots
                                              for c in other_courses & ttmodel.wdb.compatible_courses[slot2])
                    amphi_slot2 = ttmodel.sum(ttmodel.TT[slot2, c]
                                              for slot2 in successive_slots
                                              for c in amphis & ttmodel.wdb.compatible_courses[slot2])
                    broken_breaks += ttmodel.add_floor(name='', expr=amphi_slot1+other_slot2, floor=2, bound=2)
                    broken_breaks += ttmodel.add_floor(name='', expr=amphi_slot2+other_slot1, floor=2, bound=2)

            if self.weight is None:
                ttmodel.add_constraint(broken_breaks, '==', 0, Constraint())
            else:
                cost = broken_breaks * ponderation * self.local_weight()
                ttmodel.add_to_group_cost(group, cost, week)


    def one_line_description(self):
        text = f"Il faut une pause " \
               f"entre un cours CM et un autre cours"
        try:
            text += " les " + ', '.join([wd for wd in self.weekdays])
        except ObjectDoesNotExist:
            pass
        if self.groups.exists():
            text += ' pour les groupes ' + ', '.join([group.name for group in self.groups.all()])
        else:
            text += " pour tous les groupes"

        if self.train_progs.exists():
            text += ' de ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])
        else:
            text += " de toutes les promos."
        return text