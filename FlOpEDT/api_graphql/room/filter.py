from django_filters import FilterSet, CharFilter
from base.models import Room, Department

class RoomFilter(FilterSet):
    dept = CharFilter(method = 'filter_dept')

    class Meta:
        model = Room
        fields = {
            "name" : ["icontains"]
        }

    def filter_dept(self, queryset, name, value):
        return queryset.filter(departments__in = Department.objects.filter(abbrev = value))