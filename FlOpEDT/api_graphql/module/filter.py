from django_filters import FilterSet, CharFilter, NumberFilter
from base.models import Module

class ModuleFilter(FilterSet):
    dept = CharFilter(method = 'filter_dept', required = True)
    week = NumberFilter(method = 'filter_week')
    # pas de filtre year
    
    class Meta:
        model = Module
        fields = {
            'name': ['icontains', 'istartswith'],
            'abbrev': ['exact'],
            'ppn' : ['icontains'],
            'head__username' : ['exact'],
            'head__first_name' : ['icontains'],
            'train_prog__abbrev': ['exact'],
            'period__name': ['exact'],
            'url' : ['exact', 'icontains'],
        }
        exclude = ('description',)

    def filter_dept(self, queryset, name, value):
        if queryset.filter(period__department = None).count() == 0:
            return queryset.filter(period__department__abbrev = value)
        elif queryset.filter(train_prog__department = None) == 0:
            return queryset.filter(train_prog__department__abrev = value)
        else:
            return Module.objects.none()

    def filter_week(self, queryset, name, value):
        if value > 53 or value < 0:
            return Module.objects.none()
        else:
            return queryset.filter(period__starting_week__lte = value, period__ending_week__gte = value)