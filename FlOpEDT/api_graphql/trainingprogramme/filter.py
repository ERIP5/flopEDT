from django_filters import FilterSet, CharFilter
from base.models import TrainingProgramme

class TrainingProgrammeFilter(FilterSet):
    dept = CharFilter(required = True, method = 'filter_dept')

    class Meta:
        model = TrainingProgramme
        fields = {
            'abbrev': ['exact']
        }

    def filter_dept(self, queryset, name, value):
        if queryset.filter(department = None).count() == 0:
            return queryset.filter(department__abbrev = value)
        else:
            return TrainingProgramme.objects.none()