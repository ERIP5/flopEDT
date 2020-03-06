# -*- coding: utf-8 -*-
"""
Python versions: Python 3.6

This file is part of the FlOpEDT/FlOpScheduler project.
Copyright (c) 2017
Authors: Iulian Ober, Paul Renaud-Goud, Pablo Seban, et al.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with this program. If not, see
<http://www.gnu.org/licenses/>.

You can be released from the requirements of the license by purchasing
a commercial license. Buying such a license is mandatory as soon as
you develop activities involving the FlOpEDT/FlOpScheduler software
without disclosing the source code of your own applications.


This module is used to establish the crud back-end interface.
"""

import json
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from base.models import Department
from flopeditor.cruds import rooms

def good_request(request, department):
    """ Request rights verification
    :param request: Client request.
    :type request:  django.http.HttpRequest
    :param department: Department.
    :type department:  base.models.Department
    :return: true if the user has the right access to do the request
    :rtype:  boolean
    """
    if request.method == 'GET':
        return not request.user.is_anonymous and request.user.is_tutor
    return not request.user.is_anonymous and \
    request.user.has_department_perm(department, admin=True)


def crud_rooms(request, department_abbrev):
    """Crud url for rooms edition

    :param request: Client request.
    :type request:  django.http.HttpRequest
    :return: Server response for the request.
    :rtype:  django.http.JsonResponse

    """
    department = get_object_or_404(Department, abbrev=department_abbrev)
    if not good_request(request, department):
        return HttpResponseForbidden()


    if request.method == "GET":
        return rooms.read(department)
    elif request.method == "POST":
        actions = json.loads(request.body.decode('utf-8'))['actions']
        result = []
        for action in actions:
            if action['request'] == 'NEW':
                result.append(rooms.create(action, department))
            elif action['request'] == 'MODIFIED':
                result.append(rooms.update(action, department))
            elif action['request'] == 'DELETED':
                result.append(rooms.delete(action, department))
        return JsonResponse({
            'actions': result
        })
    return HttpResponseForbidden()
