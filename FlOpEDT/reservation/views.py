# Create your views here.

from django.forms import ModelForm
from django import forms
from django.shortcuts import render
from django.template.response import TemplateResponse

from reservation.models import Reservation, ReservationPeriod

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
            'description' : "Description de",
        }

class ReservationPeriodForm(ModelForm):
    class Meta:
        model = ReservationPeriod
        fields = ('period_type','start','ending',)
        widgets = {
            'start': DateInput(),
            'ending': DateInput(),
        }



def addReservation(request, department):
    reservation_form = ReservationForm()
    reservationP_form = ReservationPeriodForm()
    return render(request, 'reservation/form.html', {'reservation_form': reservation_form,'reservationP_form': reservationP_form})

def listReserv(req, department):
    return TemplateResponse(req,"reservation/listeReserv.html")
