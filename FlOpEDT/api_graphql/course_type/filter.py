from django_filters import FilterSet, CharFilter
from base.models import CourseType, Department

class CourseTypeFilter(FilterSet):
    dept = CharFilter(required = True, method = 'filter_dept')

    class Meta:
        model = CourseType
        fields = {
            'name' : ['icontains', 'istartswith'],
            'duration' : ['exact'],
            'pay_duration' : ['exact'],
            'graded' : ['exact'],
            'group_types__name' : ['icontains', 'istartswith']
        }

    def filter_dept(self, queryset, name, value):
        if queryset.filter(department = None).count() == 0:
            return queryset.filter(department__in = Department.objects.filter(abbrev = value))
        else:
            return CourseType.objects.none()
