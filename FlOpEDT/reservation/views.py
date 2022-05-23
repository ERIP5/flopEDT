# Create your views here.

from django.forms import ModelForm
from django import forms
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from pip._internal import req

from reservation.forms import ReservationForm, ReservationPeriodicityForm
from reservation.models import *


def addReservation(request, department):
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        periodicity_form = ReservationPeriodicityForm(request.POST)
        if reservation_form.is_valid() and periodicity_form.is_valid():
            reservation_data = reservation_form.cleaned_data
            periodicity_data = periodicity_form.cleaned_data
            if not reservation_data['has_periodicity']:
                save_reservation(reservation_data)
            else:
                check_periodicity(periodicity_data)

        else:
            return render(request, 'reservation/form.html', {'reservation_form': reservation_form,
                                                             'periodicity_form': periodicity_form})
    else:
        reservation_form = ReservationForm()
        periodicity_form = ReservationPeriodicityForm()
        return render(request, 'reservation/form.html', {'reservation_form': reservation_form,
                                                         'periodicity_form': periodicity_form})


def listReserv(req, department):
    return TemplateResponse(req, "reservation/listeReserv.html")


def check_reservation(reservation_data):
    # Si un cours est entre heure début et heure de fin : status NOK
    # more 'heure indisponible'
    indispo = reservation_data.start_time
    for(x) in allRoom:
        startDur = allRoom[x].courses.start + allRoom[x].courses.duration
        if (startDur < reservation_data.start_time or startDur > reservation_data.end_time):
            result = {'status': 'OK', 'more': ''}
            return result

        else:
            result = {'status': 'NOK', 'more': 'incorrect hour'}
            return result


def save_reservation(reservation_data):
    if check_reservation(reservation_data)['status'] == 'OK':
        pass  # appel_a_l_api...

    else:
        pass


def check_periodicity(periodicity_data):
    result = {'status': 'OK', 'ok_reservations': [], 'nok_reservations': []}
    considered_reservations = []  # fabriquer la liste des dictionnaires de type reservation_data correspondant à la périodicité demandée
    for considered_reservation in considered_reservations:
        reservation_result = check_reservation(considered_reservation)
        # if reservation_result['status'] == 'OK':

    # return result
