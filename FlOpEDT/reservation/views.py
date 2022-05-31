# Create your views here.

from django.forms import ModelForm
from django import forms
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from pip._internal import req
from base.models import Room, ScheduledCourse
from base.timing import days_list
from django.http import HttpResponse

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
                if save_reservation(reservation_data)=='OK':
                    return HttpResponse('yahou')
                #redirect(page basique + message pop up)
                else:
                    return HttpResponse('reservation impossible')
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
    #convert time field in minute
    start_min = reservation_data['start_time'].hour*60 + reservation_data['start_time'].minute
    end_min = reservation_data['end_time'].hour*60 + reservation_data['end_time'].minute

    #date
    good_day_nb = reservation_data['date'].weekday()
    good_day = days_list[good_day_nb - 1]
    good_year_nb = reservation_data['date'].year
    good_week_nb = reservation_data['date'].isocalendar()[1]

    #filter
    all_courses= ScheduledCourse.objects.filter(work_copy=0)
    good_time = all_courses.filter(day=good_day,
                                   course__week__nb=good_week_nb,
                                   course__week__year=good_year_nb,
                                   room__name=reservation_data['room'])

    for sched_course in good_time:
        start_course = sched_course.start_time
        end_course = sched_course.start_time + sched_course.course.type.duration
        #if (start_dur >= start_min or start_dur <= end_min):
        #if self.start_time < other.end_time and other.start_time < self.end_time:
        if (start_course < start_min and end_course > start_min) or (start_course > start_min and start_course < end_min):
            result = {'status': 'NOK', 'more': 'unavailable hour'}
            return result

    result = {'status': 'OK', 'more': ''}
    return result


def save_reservation(reservation_data):
    if check_reservation(reservation_data)['status'] == 'OK':
        return 'OK'

    else:
        return 'NOK'


def check_periodicity(periodicity_data):
    result = {'status': 'OK', 'ok_reservations': [], 'nok_reservations': []}
    considered_reservations = []  # fabriquer la liste des dictionnaires de type reservation_data correspondant à la périodicité demandée
    for considered_reservation in considered_reservations:
        reservation_result = check_reservation(considered_reservation)
        # if reservation_result['status'] == 'OK':

    # return result
