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

import django_filters.rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator

import base.models as bm
from base import queries, weeks
import people.models as pm
import displayweb.models as dwm

from api.fetch import serializers
from api.shared.params import dept_param, week_param, year_param, user_param, \
    work_copy_param
from api.permissions import IsTutorOrReadOnly, IsAdminOrReadOnly

class ScheduledCourseFilterSet(filters.FilterSet):
    dept = filters.CharFilter(field_name='course__module__train_prog__department__abbrev', required=True)
    # by promo and groups
    train_prog = filters.CharFilter(field_name='course__module__train_prog__abbrev')
    # group or tutor
    group = filters.CharFilter(field_name='course__groups__name')
    tutor_name = filters.CharFilter(field_name='tutor__username')
    # makes the fields required
    week = filters.NumberFilter(field_name='course__week', required=True)
    year = filters.NumberFilter(field_name='course__year', required=True)

    work_copy = filters.NumberFilter(field_name='work_copy')

    class Meta:
        model = bm.ScheduledCourse
        fields = ['dept', 'week', 'year']


class ScheduledCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to see all the scheduled courses

    Result can be filtered by function ScheduledCourseFilterSet
    as wanted with week, year and work_copy (0 by default).
    Request needs a department filter.
    """
    permission_classes = [IsAdminOrReadOnly]
    queryset = bm.ScheduledCourse.objects.all()\
                                         .select_related('course__module__train_prog__department',
                                                         'tutor',
                                                         'course__type',
                                                         'course__room_type',
                                                         'course__module__display')\
                                         .prefetch_related('course__groups__train_prog',
                                                           'room')
    serializer_class = serializers.ScheduledCoursesSerializer
    filter_class = ScheduledCourseFilterSet


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[
                          week_param(),
                          year_param(),
                          dept_param(),
                          work_copy_param()
                      ])
                  )
class UnscheduledCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to see all the unscheduled courses

    Result can be filtered as wanted with week, year, work_copy and department fields.
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = serializers.UnscheduledCoursesSerializer

    def get_queryset(self):
        # Creating querysets of all courses and all scheduled courses
        queryset_course = bm.Course.objects.all()
        queryset_sc = bm.ScheduledCourse.objects.all()

        # Getting filters from the URL params (?param1=...&param2=...&...)
        year = self.request.query_params.get('year', None)
        week = self.request.query_params.get('week', None)
        work_copy = self.request.query_params.get('work_copy', 0)
        department = self.request.query_params.get('dept', None)

        # Filtering different querysets
        if year is not None:
            queryset_course = queryset_course.filter(year=year)

        if week is not None:
            queryset_course = queryset_course.filter(week=week)

        queryset_sc = queryset_sc.filter(work_copy=work_copy)
        if department is not None:
            queryset_course = queryset_course.filter(module__train_prog__department__abbrev=department)
            queryset_sc = queryset_sc.filter(course__module__train_prog__department__abbrev=department)

        # Getting courses values of ScheduledCourse objects
        queryset_sc = queryset_sc.values('course')

        # Finding unscheduled courses
        queryset = queryset_course.exclude(pk__in=queryset_sc)

        return queryset


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[week_param(), year_param(), dept_param()])
                  )
class AvailabilitiesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to see all the availabilities of the tutors.

    Result can be filtered as wanted with week, year and department fields.
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = serializers.AvailabilitiesSerializer

    def get_queryset(self):
        # Getting all the wanted data
        qs = bm.UserPreference.objects.all()

        # Getting all the filters
        week = self.request.query_params.get('week', None)
        year = self.request.query_params.get('year', None)
        dept = self.request.query_params.get('dept', None)

        # Filtering
        if week is not None:
            qs = qs.filter(week=week)
        if year is not None:
            qs = qs.filter(year=year)
        if dept is not None:
            qs = qs.filter(user__departments__abbrev=dept)

        return qs


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[
                          openapi.Parameter('course_type',
                                            openapi.IN_QUERY,
                                            description="Type of course",
                                            type=openapi.TYPE_STRING),
                          openapi.Parameter('train_prog',
                                            openapi.IN_QUERY,
                                            description="Training Program",
                                            type=openapi.TYPE_STRING),
                          dept_param()
                      ])
                  )
class CourseTypeDefaultWeekViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to see all the Preferences of a given course type in a training program

    Result can be filtered as wanted with the training program and the course type
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = serializers.CourseTypeDefaultWeekSerializer

    def get_queryset(self):
        # Getting the wanted data
        qs = bm.CoursePreference.objects.all()

        # Getting all the filters
        train_prog = self.request.query_params.get('train_prog', None)
        course_type = self.request.query_params.get('course_type', None)
        department = self.request.query_params.get('dept', None)

        # Filtering
        if department is not None:
            qs = qs.select_related('train_prog__department')\
                   .filter(train_prog__department__abbrev=department)
        if train_prog is not None:
            qs = qs.filter(train_prog__abbrev=train_prog)
        if course_type is not None:
            qs = qs.filter(course_type__name=course_type)
        return qs.select_related('course_type', 'train_prog')


class AllVersionsFilterSet(filters.FilterSet):
    permission_classes = [IsAdminOrReadOnly]
    dept = filters.CharFilter(field_name='department__abbrev')

    class Meta:
        model = bm.EdtVersion
        fields = ['dept']


class AllVersionsViewSet(viewsets.ModelViewSet):
    """
    ViewSet to see all the versions of the Scheduler

    Result can be filtered as wanted with the department
    by using the function AllVersionsFilterSet
    """
    permission_classes = [IsAdminOrReadOnly]

    queryset = bm.EdtVersion.objects.all()
    serializer_class = serializers.AllVersionsSerializer
    filter_class = AllVersionsFilterSet


class DepartmentsViewSet(viewsets.ModelViewSet):
    """
    ViewSet to see all the departments

    Can be filtered as wanted with every field of a Department object.
    """
    permission_classes = [IsAdminOrReadOnly]

    queryset = bm.Department.objects.all()
    serializer_class = serializers.DepartmentAbbrevSerializer

    filterset_fields = '__all__'


class TutorCoursesFilterSet(filters.FilterSet):
    tutor_name = filters.CharFilter(field_name='user__departments__train_prog__module__module__tutor__username',
                                    required=True)
    year = filters.CharFilter(field_name='user__departments__train_prog__module__module__year')
    week = filters.CharFilter(field_name='user__departments__train_prog__module__module__week')
    dept = filters.CharFilter(field_name='user__departments__abbrev')

    class Meta:
        model = pm.UserDepartmentSettings
        fields = ['tutor_name', 'year', 'week', 'dept']


class TutorCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to see all the courses of a tutor

    Result needs to be filtered by the username of a tutor.
    Filtering is also possible with week, department and year.
    """
    permission_classes = [IsAdminOrReadOnly]

    serializer_class = serializers.TutorCourses_Serializer
    queryset = pm.UserDepartmentSettings.objects.all()
    filter_class = TutorCoursesFilterSet


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[week_param(), year_param(), user_param(required=True),
                                         dept_param(required=True)])
                  )
class ExtraSchedCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to see all the Scheduled courses of a tutor in an other department

    Result can be filtered with year and week
    """
    permission_classes = [IsAdminOrReadOnly]

    serializer_class = serializers.ExtraScheduledCoursesSerializer
    permission_classes = [IsTutorOrReadOnly]

    def get_queryset(self):
        qs_esc = bm.ScheduledCourse.objects.all()
        # Getting all the filters
        user = self.request.query_params.get('username', None)
        dept = self.request.query_params.get('dept', None)
        week = self.request.query_params.get('week', None)
        year = self.request.query_params.get('year', None)

        # Filtering
        if user is None:
            return None
        if dept is None:
            return None

        if week is not None:
            qs_esc = qs_esc.filter(course__week=week)
        if year is not None:
            qs_esc = qs_esc.filter(course__year=year)

        # Getting all the needed data

        return qs_esc.filter(course__tutor__username=user)\
                     .exclude(course__module__train_prog__department__abbrev=dept)\
                     .select_related('course__tutor',
                                     'course__type__department',
                                     'course__module__train_prog__department')



class BKNewsFilterSet(filters.FilterSet):
    permission_classes = [IsTutorOrReadOnly]
    dept = filters.CharFilter(field_name='department__abbrev', required=True)
    # makes the fields required
    week = filters.NumberFilter(field_name='week', required=True)
    year = filters.NumberFilter(field_name='year', required=True)

    class Meta:
        model = dwm.BreakingNews
        fields = ['dept', 'week', 'year']


class BKNewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet to see all the BKNews

    Result needs to be filtered by the department,the week and the year.
    """
    permission_classes = [IsAdminOrReadOnly]

    queryset = dwm.BreakingNews.objects.all()
    serializer_class = serializers.BKNewsSerializer
    filter_class = BKNewsFilterSet


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[week_param(required=True),
                                         year_param(required=True),
                                         dept_param(required=True)]),

                  )
class UnavailableRoomViewSet(viewsets.ViewSet):
    """
    Allow user to search for unavailable rooms for a given year, week and department

    Each result contains room name, day, start_time, duration, and value (unavailable => 0)
    """
    permission_classes = [IsAdminOrReadOnly]

    def list(self, req, format=None):

        try:
            week = int(req.query_params.get('week'))
            year = int(req.query_params.get('year'))
            department = req.query_params.get('dept')
            if department == 'None':
                department = None
        except ValueError:
            return HttpResponse("KO")

        # ----------------
        # To be done later
        # ----------------
        #
        # cache_key = get_key_unavailable_rooms(department.abbrev, year, week)
        # cached = cache.get(cache_key)
        # if cached is not None:
        #     return cached

        dataset = bm.RoomPreference.objects.filter(room__departments__abbrev=department,
                                                   week=week,
                                                   year=year,
                                                   value=0)

        # cache.set(cache_key, response)7
        res = [{"room": d.room.name, "day": d.day, "start_time": d.start_time, "duration": d.duration, "value": d.value}
               for d in dataset]

        return Response(res)


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[dept_param(required=True)]),

                  )
class ConstraintsQueriesViewSet(viewsets.ViewSet):
    """
    Return course type constraints for a given department
    """
    permission_classes = [IsAdminOrReadOnly]

    def list(self, req):
        try:
            department = req.query_params.get('dept')
            if department == 'None':
                department = None
        except ValueError:
            return HttpResponse("KO")

        constraints = queries.get_coursetype_constraints(department)
        return JsonResponse(constraints, safe=False)


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[
                          week_param(required=True),
                          year_param(required=True),
                          dept_param(required=True)
                      ]
                  ),
                  )
class WeekDaysViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminOrReadOnly]

    def list(self, req):
        week = int(req.query_params.get('week'))
        year = int(req.query_params.get('year'))
        try:
            department = bm.Department.objects.get(
                abbrev=req.query_params.get('dept', None)
            )
        except bm.Department.DoesNotExist:
            raise exceptions.NotFound(detail='Department not found')

        data = weeks.num_all_days(year, week, department)
        return JsonResponse(data, safe=False)