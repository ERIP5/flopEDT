from django_filters import FilterSet, CharFilter
from base.models import UserPreference, Department

class UserPreferenceFilter(FilterSet):
    dept = CharFilter(method = 'filter_dept')

    class Meta:
        model = UserPreference
        fields = {
            'user__username' : ['exact', 'icontains'],
            'user__first_name' : ['icontains', 'istartswith'], 
            'week__nb' : ['exact'], 
            'week__year' : ['exact']
        }

    def filter_dept(self, queryset, name, value):
        return queryset.filter(user__departments__in = Department.objects.filter(abbrev = value))