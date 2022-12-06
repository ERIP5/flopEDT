from django_filters import FilterSet, NumberFilter
from base.models import ScheduledCourse

class ScheduledCourseFilter(FilterSet):
    week = NumberFilter(required = True, method = 'filter_week')
    year = NumberFilter(required = True, method = 'filter_year') 
    
    class Meta:
        model = ScheduledCourse
        fields = {
            'room__name': ['icontains', 'istartswith'],
            'day': ['exact'],
            'course__module__abbrev': ['icontains', 'istartswith'],
            'tutor__username': ['icontains', 'istartswith'],
            'start_time' : ['exact'],
            'number' : ['exact'],
            'noprec': ['exact'],
            'work_copy': ['exact']
        }
    
    def filter_week(self, queryset, name, value):
        if queryset.filter(course__week = None).count() == 0:     
            return queryset.filter(course__week__nb = value)
        else:
            return ScheduledCourse.objects.none()

    def filter_year(self, queryset, name, value):
        if queryset.filter(course__week = None).count() == 0:     
            return queryset.filter(course__week__year = value)
        else:
            return ScheduledCourse.objects.none() 
    
