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
from django.utils.decorators import method_decorator
import django_filters.rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import people.models as pm
import base.models as bm
from api.people import serializers
from api.shared.params import week_param, year_param
from api.shared.views_set import ListGenericViewSet


class UsersViewSet(viewsets.ModelViewSet):
    """
    ViewSet to see all the users

    Can be filtered as wanted with every field of a User object.
    """
    permission_classes = (IsAuthenticated,)
    queryset = pm.User.objects.all()
    serializer_class = serializers.UsersSerializer


class UserDepartmentSettingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet to see all the user department settings
    which shows the combination of the user and the department

    Can be filtered as wanted with every field of a User Department object.
    """
    queryset = pm.UserDepartmentSettings.objects.all()
    serializer_class = serializers.UserDepartmentSettingsSerializer


class SupplyStaffsViewSet(viewsets.ModelViewSet):
    """
    ViewSet to see all the supply staff

    Can be filtered as wanted with every field of a Supply Staff object.
    """
    queryset = pm.SupplyStaff.objects.all()
    serializer_class = serializers.SupplyStaffsSerializer


class StudentsViewSet(viewsets.ModelViewSet):
    """
    ViewSet to see all the students

    Can be filtered as wanted with every field of a Student object.
    """
    queryset = pm.Student.objects.all()
    serializer_class = serializers.StudentsSerializer


class TutorFilterSet(filters.FilterSet):
    dept = filters.CharFilter(field_name='departments__abbrev', required=True)

    class Meta:
        model = pm.Tutor
        fields = ['dept']


class TutorUsernameViewSet(viewsets.ModelViewSet):
    """
    ViewSet to see all the tutors

    Can be filtered as wanted with every field of a Tutor object.
    """
    queryset = pm.Tutor.objects.all()
    serializer_class = serializers.TutorUsernameSerializer
    filter_class = TutorFilterSet


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      operation_description="Active tutors",
                      manual_parameters=[week_param(), year_param()])
                  )
class TutorViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Getting all the filters
        week = self.request.query_params.get('week', None)
        year = self.request.query_params.get('year', None)

        # Filtering
        if week is not None and year is not None:
            return pm.Tutor.objects.filter(
                pk__in=bm.ScheduledCourse.objects.filter(
                    course__week=week,
                    course__year=year) \
                    .distinct('tutor').values('tutor')
            )
        else:
            return pm.Tutor.objects.all()

    serializer_class = serializers.TutorSerializer
    filter_class = TutorFilterSet


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      operation_description="Get current user")
                  )
class CurrentUserViewSet(ListGenericViewSet):
    queryset = pm.User.objects.all()
    serializer_class = serializers.UserSerializer

    @permission_classes([IsAuthenticated])
    def list(self, request):
        queryset = request.user
        serializer = serializers.UserSerializer(queryset)
        print(self.request)
        print(self.request.auth)
        print(self.request.user)
        print(queryset)
        return Response(serializer.data)
