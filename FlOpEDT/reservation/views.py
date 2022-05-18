# Create your views here.

from django.forms import ModelForm
from django import forms
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from pip._internal import req

from reservation.forms import ReservationForm
from reservation.models import *

def addReservation(request, department):
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            reserva = reservation_form.save()
            return redirect("http://localhost:8000/fr/reservation/INFO/listeReserv")
    else:
        reservation_form = ReservationForm()

    return render(request, 'reservation/form.html', {'reservation_form': reservation_form})

def listReserv(req, department):
    return TemplateResponse(req,"reservation/listeReserv.html")
