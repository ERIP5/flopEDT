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

from django.db import models

from TTapp.helpers.minhalfdays import MinHalfDaysHelperGroup

from TTapp.slots import slots_filter
from TTapp.TTConstraint import TTConstraint

def considered_basic_groups(group_ttconstraint, ttmodel):
    if group_ttconstraint.train_progs.exists():
        considered_basic_groups = set(ttmodel.wdb.basic_groups.filter(train_prog__in=group_ttconstraint.train_progs.all()))
    else:
        considered_basic_groups = set(ttmodel.wdb.basic_groups)
    if group_ttconstraint.groups.exists():
        basic_groups = set()
        for g in group_ttconstraint.groups.all():
            basic_groups |= g.basic_groups()
        considered_basic_groups &= basic_groups
    return considered_basic_groups


class MinGroupsHalfDays(TTConstraint):
    """
    All courses will fit in a minimum of half days
    """
    groups = models.ManyToManyField('base.Group', blank=True)

    def enrich_model(self, ttmodel, week, ponderation=1):
        helper = MinHalfDaysHelperGroup(ttmodel, self, week, ponderation)
        for group in considered_basic_groups(self, ttmodel):
            helper.enrich_model(group=group)

    def get_viewmodel(self):
        view_model = super().get_viewmodel()
        details = view_model['details']

        if self.groups.exists():
            details.update({'groups': ', '.join([group.name for group in self.groups.all()])})

        return view_model

    def one_line_description(self):
        text = "Minimise les demie-journées"

        if self.groups.exists():
            text += ' des groupes ' + ', '.join([group.name for group in self.groups.all()])
        else:
            text += " de tous les groupes"

        if self.train_progs.exists():
            text += ' de ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])
        else:
            text += " de toutes les promos."

        return text


class MinNonPreferedTrainProgsSlot(TTConstraint):
    """
    Minimize the use of unprefered Slots for groups
    """
    def enrich_model(self, ttmodel, week, ponderation=None):
        if ponderation is None:
            ponderation = ttmodel.min_ups_c
        if self.train_progs.exists():
            train_progs = set(tp for tp in self.train_progs.all() if tp in ttmodel.train_prog)
        else:
            train_progs = set(ttmodel.train_prog)
        for train_prog in train_progs:
            basic_groups = ttmodel.wdb.basic_groups.filter(train_prog=train_prog)
            for g in basic_groups:
                g_pref = g.preferences
                g_pref.calculate_fields()
                morning_weight = 2 * g_pref.get_morning_weight()
                evening_weight = 2 * g_pref.get_evening_weight()
                light_day_weight = 2 * g_pref.get_light_day_weight()
                for sl in ttmodel.wdb.availability_slots:
                    day_time_ponderation = light_day_weight
                    if sl in ttmodel.wdb.morning_slots:
                        day_time_ponderation *= morning_weight
                    elif sl in ttmodel.wdb.evening_slots:
                        day_time_ponderation *= evening_weight

                    for c in ttmodel.wdb.courses_for_basic_group[g]:
                        slot_vars_sum = ttmodel.sum(ttmodel.TT[(sl2, c)]
                                                    for sl2 in slots_filter(ttmodel.wdb.compatible_slots[c],
                                                                            simultaneous_to=sl))
                        cost = self.local_weight() * ponderation * slot_vars_sum \
                            * ttmodel.unp_slot_cost_course[c.type,
                                                           train_prog][sl]
                        cost *= day_time_ponderation
                        ttmodel.add_to_group_cost(g, cost, week=week)

    def one_line_description(self):
        text = "Respecte les préférences"
        if self.train_progs.exists():
            text += ' des groupes de ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])
        else:
            text += ' de toutes les promos.'
        return text
