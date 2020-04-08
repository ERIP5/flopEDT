#!/usr/bin/env python3
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

import importlib

import pulp.solvers as pulp_solvers

from TTapp.TTModel import TTModel, GUROBI_NAME

from MyFlOp.MyTTUtils import print_differences
from MyFlOp.iut_specific_constraints import add_iut_specific_constraints


class MyTTModel(TTModel):
    def __init__(self, department_abbrev, weeks, year,
                 train_prog=None,
                 stabilize_work_copy=None,
                 min_nps_i=1.,
                 min_bhd_g=1.,
                 min_bd_i=1.,
                 min_bhd_i=1.,
                 min_nps_c=1.,
                 max_stab=5.,
                 lim_ld=1.,
                 core_only=False,
                 send_mails=False):
        """
        If you shall change something in the database ahead of creating the
        problem, you must write it here, before calling TTModel's constructor.

        """
        TTModel.__init__(self, department_abbrev, weeks, year,
                         train_prog=train_prog,
                         stabilize_work_copy=stabilize_work_copy,
                         min_nps_i=min_nps_i,
                         min_bhd_g=min_bhd_g,
                         min_bd_i=min_bd_i,
                         min_bhd_i=min_bhd_i,
                         min_nps_c=min_nps_c,
                         max_stab=max_stab,
                         lim_ld=lim_ld,
                         core_only=core_only,
                         send_mails=send_mails)

    def add_specific_constraints(self):
        """
        The speficic constraints stored in the database are added by the
        TTModel class.
        If you shall add more specific ones, you may write it down here.
        """
        TTModel.add_specific_constraints(self)
        add_iut_specific_constraints(self)

    def solve(self, time_limit=3600, target_work_copy=None,
              solver=GUROBI_NAME):
        """
        If you shall add pre (or post) processing apps, you may write them down
        here.
        """
        result = TTModel.solve(self,
                               time_limit=time_limit,
                               target_work_copy=target_work_copy,
                               solver=solver)
        if result is not None and self.stabilize_work_copy is not None:
            print_differences(self.weeks, self.year, self.stabilize_work_copy, target_work_copy, self.wdb.instructors)
