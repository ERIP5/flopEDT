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

from TTapp.ilp_constraints.constraint_type import ConstraintType
from TTapp.ilp_constraints.constraint import Constraint
from TTapp.slots import days_filter, slots_filter
from TTapp.TTConstraint import TTConstraint
from TTapp.TTConstraints.groups_constraints import considered_basic_groups
from base.timing import Day
from django.contrib.postgres.fields import ArrayField


class NoVisio(TTConstraint):
    weekdays = ArrayField(models.CharField(max_length=2, choices=Day.CHOICES), blank=True, null=True)
    groups = models.ManyToManyField('base.Group', blank=True, related_name='no_visio')

    def enrich_model(self, ttmodel, week, ponderation=1000000):
        visio = ttmodel.wdb.visio_room
        considered_groups = considered_basic_groups(self, ttmodel)
        days = days_filter(ttmodel.wdb.days, week=week)
        if self.weekdays:
            days = days_filter(days, day_in=self.weekdays)
        for group in considered_groups:
            ttmodel.add_constraint(
                ttmodel.sum(ttmodel.TTrooms[sl,c,visio]
                            for c in ttmodel.wdb.courses_for_basic_group[group]
                            for sl in slots_filter(ttmodel.wdb.compatible_slots[c], day_in=days)),
                '==', 0, Constraint(constraint_type=ConstraintType.VISIO, groups=group))

    def one_line_description(self):
        text = "Pas de visio"
        if self.weekdays:
            text += " les " + ', '.join([wd for wd in self.weekdays])
        if self.groups.exists():
            text += ' pour les groupes ' + ', '.join([group.name for group in self.groups.all()])
        else:
            text += " pour tous les groupes"

        if self.train_progs.exists():
            text += ' de ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])
        else:
            text += " de toutes les promos."
        return text