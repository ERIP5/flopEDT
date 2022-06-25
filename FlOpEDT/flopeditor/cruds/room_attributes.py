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

"""

from django.http import JsonResponse
from base.models import Room, RoomAttribute
from flopeditor.validator import OK_RESPONSE, ERROR_RESPONSE


def read(department):
    """Return all room attributes
    :return: Server response for the request.

    """

    room_attributes = RoomAttribute.objects.all()

    values = []
    for attribute in room_attributes:
        values.append((attribute.name, attribute.description))

    return JsonResponse({
        "columns" :  [{
            'name': 'Attributs',
            "type": "text",
            "options": {}
        }, {
            'name': 'Description',
            "type": "text",
            "options": {}
        }],
        "values" : values,
        "options": { "examples": [
                ["Attribut1","description1"],
                ["Attribut2","description2"]
            ]
        }
    })


def create(entries, department):
    """Create values for room types
    :param entries: Values to create.
    :type entries:  django.http.JsonResponse
    :param department: Department.
    :type department:  base.models.Department
    :return: Server response for the request.
    :rtype:  django.http.JsonResponse
    """

    entries['result'] = []
    for i in range(len(entries['new_values'])):
        new_name = entries['new_values'][i][0]
        new_description = entries['new_values'][i][1]
        if not new_name:
            entries['result'].append([
                ERROR_RESPONSE,
                "Le nom du type de salle à ajouter est vide."
            ])
        elif len(new_name) > 20:
            entries['result'].append([
                ERROR_RESPONSE,
                "Le nom de l'attribut  à ajouter est trop long."
            ])
        elif RoomAttribute.objects.filter(name=new_name).exists():
            entries['result'].append([
                ERROR_RESPONSE,
                "L'attribut à ajouter est déjà présent dans la base de données."
            ])
        else:
            room_type = RoomAttribute.objects.create(name=new_name, description=new_description)
    return entries


def update(entries, department):
    """Update values for room types
    :param entries: Values to modify.
    :type entries:  django.http.JsonResponse
    :return: Server response for the request.
    :rtype:  django.http.JsonResponse
    """

    entries['result'] = []
    if len(entries['old_values']) != len(entries['new_values']):
        # old and new values must have same size
        return entries
    for i in range(len(entries['old_values'])):
        old_name = entries['old_values'][i][0]
        new_name = entries['new_values'][i][0]
        new_description = entries['new_values'][i][1]
        if not new_name:
            entries['result'].append([
                ERROR_RESPONSE,
                "Le nom du type de salle à modifier est vide."
            ])
        elif len(new_name) > 20:
            entries['result'].append([
                ERROR_RESPONSE,
                "Le nom de l'attribut à est trop long."
            ])
        elif old_name != new_name and RoomAttribute.objects.filter(name=new_name).exists():
            entries['result'].append(
                [ERROR_RESPONSE,
                 "Le nom de cet attribut est déjà utilisé."])
        else:
            try:
                rt_to_update = RoomAttribute.objects.get(name=old_name)
                rt_to_update.name = new_name
                rt_to_update.descriptipon = new_description
                rt_to_update.save()
            except RoomAttribute.DoesNotExist:
                entries['result'].append(
                    [ERROR_RESPONSE,
                     "Un attribut à modifier n'a pas été trouvé dans la base de données."])

    return entries


def delete(entries, department):
    """Delete values for room types
    :param entries: Values to delete.
    :type entries:  django.http.JsonResponse
    :param department: Department.
    :type department:  base.models.Department
    :return: Server response for the request.
    :rtype:  django.http.JsonResponse
    """
    entries['result'] = []
    for i in range(len(entries['old_values'])):
        old_name = entries['old_values'][i][0]
        try:
            RoomAttribute.objects.get(name=old_name).delete()
            entries['result'].append([OK_RESPONSE])
        except RoomAttribute.DoesNotExist:
            entries['result'].append(
                [ERROR_RESPONSE,
                 "Un attribut à supprimer n'a pas été trouvé dans la base de données."])
    return entries
