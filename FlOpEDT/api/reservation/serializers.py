from colorfield.fields import ColorField
from rest_framework import serializers

import reservation.models as rm
import api.fetch.serializers as fs


class ReservationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    responsible = serializers.CharField()
    room = fs.ResRoomSerializer()
    title = serializers.CharField()
    description = serializers.CharField()
    with_key = serializers.BooleanField()
    email = serializers.BooleanField()
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    class Meta:
        model = rm.Reservation
        fields = '__all__'

class ReservationTSerializer(serializers.Serializer):
    name = serializers.CharField()
    bg_color = serializers.CharField()

    class Meta:
        model = rm.ReservationType
        fields = '__all__'
