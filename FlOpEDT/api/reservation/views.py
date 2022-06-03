from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from api.reservation import serializers
import reservation.models as rm
from api.shared.params import week_param, year_param


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[
                          # in the filterset
                          week_param(),
                          year_param()
                      ])
                  )
class ReservationViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ReservationSerializer

    def get_queryset(self):
        all_res = rm.Reservation.objects.all()
        week = self.request.query_params.get('week', None)
        year = self.request.query_params.get('year', None)

        if week is not None:
            all_res = all_res.filter(date__week =week)
        if year is not None:
            all_res = all_res.filter(date__year=year)

        return all_res

    filterset_fields = '__all__'

class ReservationTViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ReservationTSerializer
    queryset = rm.ReservationType.objects.all()
    filterset_fields = '__all__'
