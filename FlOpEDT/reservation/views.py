# Create your views here.

from django.forms import ModelForm
from django import forms
from django.shortcuts import render

from reservation.models import Reservation, Reservation_periode

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ('responsible','reservation_type','title','description','key','reservation_date','start','duration','room',)
        widgets = {
            'reservation_date': DateInput(),
            'start': TimeInput(),
            'duration': TimeInput(),
        }
        labels = {
            'responsible': "Choisir un responsable",
            'title': "description breve de la réservation",
        }

class ReservationPeriodForm(ModelForm):
    class Meta:
        model = Reservation_periode
        fields = ('period_type','start','ending',)
        widgets = {
            'start': DateInput(),
            'ending': DateInput(),
        }



def Reservation(request):
    reservation_form = ReservationForm()
    reservationP_form = ReservationPeriodForm()
    return render(request, 'reservation/form.html', {'reservation_form': reservation_form,'reservationP_form': reservationP_form})

