from django_filters import FilterSet, CharFilter
from base.models import Course

class CourseFilter(FilterSet):
    dept = CharFilter(method = 'filter_dept')
    class Meta:
        model = Course
        fields = {
                    'type__name' : ['icontains', 'istartswith'],
                    'room_type__name' : ['icontains', 'istartswith'],
                    'no' : ['exact'],
                    'tutor__username' : ['exact'],
                    'tutor__first_name' : ['icontains', 'istartswith'],
                    'supp_tutor__username' : ['exact'],
                    'supp_tutor__first_name' : ['icontains', 'istartswith'],
                    'groups__name' : ['icontains', 'istartswith'],
                    'module__name' : ['icontains', 'istartswith'],
                    'module__abbrev' : ['exact'],
                    'modulesupp__name' : ['icontains', 'istartswith'],
                    'modulesupp__abbrev' : ['exact'],
                    'pay_module__name' : ['icontains', 'istartswith'],
                    'pay_module__abbrev' : ['exact'],
                    'week__nb' : ['exact'],
                    'week__year' : ['exact']
        }
        exclude = ('suspens', 'show_id')
    
    def filter_dept(self, queryset, name, value):
        if queryset.filter(type__department = None).count() == 0:
            return queryset.filter(type__department__abbrev = value)
        elif queryset.filter(room_type = None).count() == 0:
            return queryset.filter(room_type__department__abbrev = value)
        elif queryset.filter(module__train_prog__department = None) == 0:
            return queryset.filter(module__train_prog__department__abrev = value)
        else:
            return Course.objects.none()
