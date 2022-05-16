# Create your views here.

from django.forms import ModelForm
from django import forms
from django.shortcuts import render
from django.template.response import TemplateResponse

from reservation.models import *


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"
        widgets = {
            'reservation_date': DateInput(),
            'start': TimeInput(),
            'duration': TimeInput(),
            'Period_choice': forms.RadioSelect(choices=period_choice),
            'ed_period': DateInput()

        }
        labels = {
            'responsible': "Responsible's name",
            'title': "Title of reservation",
            'description': "Description",
            'key': "Borrowed key",
            'courriel': "Send confirmation courriel",
            'periodicity': "Add periodicity to the reservation",
            'ed_period': "End of the periodicity"
        }

class ReservationPeriodForm(ModelForm):
    class Meta:
        model = Reservation_periode
        fields = "__all__"
        widgets = {
            'start': DateInput(),
            'ending': DateInput()
        }



def addReservation(request, department):
    reservation_form = ReservationForm()
    reservationP_form = ReservationPeriodForm()
    return render(request, 'reservation/form.html', {'reservation_form': reservation_form,'reservationP_form': reservationP_form})

def listReserv(req, department):
    return TemplateResponse(req,"reservation/listeReserv.html")
