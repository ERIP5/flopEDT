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

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
import django_filters.rest_framework as filters

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator

import base.models as bm
from base import queries

from api.base.rooms import serializers
from api.shared.params import dept_param
from api.permissions import IsTutorOrReadOnly, IsAdminOrReadOnly

class RoomGrafanaViewSet(viewsets.ModelViewSet):
    """
    ViewSet to see all the rooms with their grafana id.

    Can be filtered as wanted with every field of a RoomGrafana object.
    """
    permission_classes = [IsAdminOrReadOnly]

    queryset = bm.RoomGrafana.objects.all()
    serializer_class = serializers.RoomGrafanaSerializer
    filterset_fields = '__all__'
