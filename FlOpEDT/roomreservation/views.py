from django.shortcuts import render
from rest_framework.reverse import reverse_lazy


def vue(request, **kwargs):
    db_data = {'dept': request.department.abbrev, 'api': reverse_lazy('api:api_root', request=request)}
    return render(request, 'roomreservation/index.html', {'json_data': db_data})
