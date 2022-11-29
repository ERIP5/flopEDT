from django_filters import FilterSet, CharFilter
from base.models import GenericGroup

class GenericGroupFilter(FilterSet):
    dept = CharFilter(required = True, method = 'filter_dept')

    class Meta:
        model = GenericGroup
        fields = {
            'name' : ['icontains', 'istartswith'],
            'train_prog__name' : ['icontains', 'istartswith'],
            'type__name' : ['icontains', 'istartswith'],
            'size' : ['exact']
        }
    
    def filter_dept(self, queryset, name, value):
        if queryset.filter(type__department = None).count() == 0:
            return queryset.filter(type__department__abbrev = value)
        elif queryset.filter(train_prog__department = None) == 0:
            return queryset.filter(train_prog__department__abrev = value)
        else:
            return GenericGroup.objects.none()
