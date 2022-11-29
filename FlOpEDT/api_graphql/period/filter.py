from django_filters import FilterSet
from base.models import Period

class PeriodFilter(FilterSet):
    class Meta:
        model = Period
        fields = {
                    'department__name' : ['icontains', 'istartswith'],
                    'name' : ['exact']
                }