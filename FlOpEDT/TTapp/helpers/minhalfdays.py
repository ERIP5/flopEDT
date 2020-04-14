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

from base.models import Time, TimeGeneralSettings
from TTapp.iic.constraint_type import ConstraintType
from TTapp.iic.constraints.constraint import Constraint


logger = logging.Logger(__name__)

class MinHalfDaysHelperBase():

    def __init__(self, ttmodel, constraint, week, ponderation):
        self.ttmodel = ttmodel
        self.constraint = constraint
        self.ponderation = ponderation
        self.week = week


    def build_variables(self):
        return None, None, None


    def add_cost(self, cost):
        pass

    
    def add_constraint(self, expression, courses, local_var):
        self.ttmodel.add_constraint(local_var, '==', 1,
                                    Constraint(constraint_type=ConstraintType.MIN_HALF_DAYS_LOCAL))
        course_time = sum(c.type.duration for c in courses)
        t = TimeGeneralSettings.objects.get(department=self.ttmodel.department)
        half_days_min_time = min(t.lunch_break_start_time-t.day_start_time, t.day_finish_time-t.lunch_break_finish_time)
        limit = (course_time - 1) // half_days_min_time + 1

        if self.constraint.weight:
            cost = self.constraint.local_weight() * self.ponderation * (expression - limit * local_var)
            self.add_cost(cost)
        else:
            self.ttmodel.add_constraint(expression, '<=', limit,
                                        Constraint(constraint_type=ConstraintType.MIN_HALF_DAYS_LIMIT))

    def enrich_model(self, **args):
        expression, courses, local_var = self.build_variables()
        self.add_constraint(expression, courses, local_var)


class MinHalfDaysHelperModule(MinHalfDaysHelperBase):

    def build_variables(self):
        days = set(day for day in self.ttmodel.wdb.days if day.week==self.week)
        mod_b_h_d = {}
        for d in days:
            mod_b_h_d[(self.module, d, Time.AM)] \
                = self.ttmodel.add_var("ModBHD(%s,%s,%s)"
                                    % (self.module, d, Time.AM))
            mod_b_h_d[(self.module, d, Time.PM)] \
                = self.ttmodel.add_var("ModBHD(%s,%s,%s)"
                                    % (self.module, d, Time.PM))
            
            # add constraint linking MBHD to TT
            for apm in [Time.AM, Time.PM]:
                halfdayslots = set(sl for sl in self.ttmodel.wdb.slots if sl.day == d and sl.apm == apm)
                card = len(halfdayslots)
                expr = self.ttmodel.lin_expr()
                expr += card * mod_b_h_d[(self.module, d, apm)]
                for sl in halfdayslots:
                    for c in set(self.ttmodel.wdb.courses.filter(module=self.module))\
                            & self.ttmodel.wdb.compatible_courses[sl]:
                        expr -= self.ttmodel.TT[(sl, c)]
                self.ttmodel.add_constraint(expr, '>=', 0,
                                            Constraint(constraint_type=ConstraintType.MIN_HALF_DAYS_SUP))
                self.ttmodel.add_constraint(expr, '<=', card - 1,
                                            Constraint(constraint_type=ConstraintType.MIN_HALF_DAYS_INF))
        
        local_var = self.ttmodel.add_var("MinMBHD_var_%s" % self.module)
        # no year?
        courses = self.ttmodel.wdb.courses.filter(module=self.module, week=self.week)
        expression = self.ttmodel.sum(
            mod_b_h_d[(self.module, d, apm)]
            for d in days
            for apm in [Time.AM, Time.PM])

        return expression, courses, local_var


    def add_cost(self, cost):        
        self.ttmodel.obj += cost


    def enrich_model(self, module=None):
        if module:
            self.module = module
            super().enrich_model()
        else:
            raise("MinHalfDaysHelperModule requires a module argument")


class MinHalfDaysHelperGroup(MinHalfDaysHelperBase):

    def build_variables(self):
        courses = self.ttmodel.wdb.courses.filter(group=self.group, week=self.week)

        expression = self.ttmodel.check_and_sum(
            self.ttmodel.GBHD,
            ((self.group, d, apm) for d, apm in self.ttmodel.wdb.slots_by_half_day if d.week==self.week))

        local_var = self.ttmodel.add_var("MinGBHD_var_%s" % self.group)

        return expression, courses, local_var


    def add_cost(self, cost):
        self.ttmodel.add_to_group_cost(self.group, cost, self.week)


    def enrich_model(self, group=None):
        if group:
            self.group = group
            super().enrich_model()
        else:
            raise Exception("MinHalfDaysHelperGroup requires a group argument")



class MinHalfDaysHelperTutor(MinHalfDaysHelperBase):

    def build_variables(self):
        # no year?
        courses = self.ttmodel.wdb.courses.filter(tutor=self.tutor, week=self.week)
        days = set(day for day in self.ttmodel.wdb.days if day.week == self.week)
        expression = self.ttmodel.sum(
            self.ttmodel.IBHD[(self.tutor, d, apm)]
            for d in days
            for apm in [Time.AM, Time.PM])
        local_var = self.ttmodel.add_var("MinIBHD_var_%s" % self.tutor)

        return expression, courses, local_var

    def add_cost(self, cost):        
        self.ttmodel.add_to_inst_cost(self.tutor, cost, self.week)

    def add_constraint(self, expression, courses, local_var):
        super().add_constraint(expression, courses, local_var)
        days = set(day for day in self.ttmodel.wdb.days if day.week == self.week)
        # Try to joincourses
        if self.constraint.join2courses and len(courses) in [2, 4]:
            for d in days:
                for c in courses:
                    sl8h = min(self.ttmodel.wdb.slots_by_half_day[d,Time.AM] & self.ttmodel.wdb.compatible_slots[c])
                    sl14h = min(self.ttmodel.wdb.slots_by_half_day[d,Time.PM] & self.ttmodel.wdb.compatible_slots[c])
                    for c2 in courses.exclude(id=c.id):
                        sl11h = max(
                            self.ttmodel.wdb.slots_by_half_day[d, Time.AM] & self.ttmodel.wdb.compatible_slots[c2])
                        sl17h = max(
                            self.ttmodel.wdb.slots_by_half_day[d, Time.PM] & self.ttmodel.wdb.compatible_slots[c2])
                        if self.constraint.weight:
                            conj_var_AM = self.ttmodel.add_conjunct(self.ttmodel.TT[(sl8h, c)],
                                                                    self.ttmodel.TT[(sl11h, c2)])
                            conj_var_PM = self.ttmodel.add_conjunct(self.ttmodel.TT[(sl14h, c)],
                                                                    self.ttmodel.TT[(sl17h, c2)])
                            self.ttmodel.add_to_inst_cost(self.tutor,
                                                          self.constraint.local_weight() * self.ponderation *
                                                          (conj_var_AM + conj_var_PM)/2,
                                                          week=self.week)
                        else:
                            self.ttmodel.add_constraint(
                                self.ttmodel.TT[(sl8h, c)] + self.ttmodel.TT[(sl11h, c2)],
                                '<=',
                                1,
                                Constraint(constraint_type=ConstraintType.MIN_HALF_DAYS_JOIN_AM))
                            self.ttmodel.add_constraint(
                                self.ttmodel.TT[(sl14h, c)] + self.ttmodel.TT[(sl17h, c2)],
                                '<=',
                                1, Constraint(constraint_type=ConstraintType.MIN_HALF_DAYS_JOIN_PM))

    def enrich_model(self, tutor=None):
        if tutor:
            self.tutor = tutor
            super().enrich_model()
        else:
            raise Exception("MinHalfDaysHelperTutor requires a tutor argument")
