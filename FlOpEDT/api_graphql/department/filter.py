from django_filters import FilterSet
from base.models import Department

class DepartmentFilter(FilterSet):
    class Meta:
        model = Department
        fields = {
            'name' : ['icontains', 'istartswith'],
            'abbrev' : ['exact']
        }