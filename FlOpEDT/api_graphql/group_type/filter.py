from django_filters import FilterSet
from base.models import GroupType

class GroupTypeFilter(FilterSet):
    class Meta:
        model = GroupType
        fields = {
            'name' : ['icontains', 'istartswith'],
            'department__name' : ['icontains', 'istartswith'],
            'department__abbrev' : ['exact']
        }
