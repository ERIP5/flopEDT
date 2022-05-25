# Create your views here.

from django.forms import ModelForm
from django import forms
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from pip._internal import req
from base.models import Room, ScheduledCourse
from base.timing import days_list

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
    #convert time field in minute
    start_min = reservation_data['start_time'].hour*60 + reservation_data['start_time'].minute
    end_min = reservation_data['end_time'].hour*60 + reservation_data['end_time'].minute

    good_day_nb = reservation_data['date'].weekday()
    good_year_nb = reservation_data['date'].year()
    good_day = days_list[good_day_nb - 1]

    good_room = Room.objects.get(name=reservation_data['room'])

    all_courses= ScheduledCourse.objects.filter(work_copy=0)
    good_time = all_courses.filter(day=good_day, course__week__nb=11, course__week_year=good_year_nb)
    #room_courses = all_courses.filter(room=good_room)
    for sched_course in good_time:
        #sched_course.start_time
        #sched_course.course.week.nb
        #sched_course.course.type.duration


        start_dur = 600
        #startDur = Room.object.get(good_room.courses.good_day[room].start) + \
        #           Room.object.get(good_room.courses.good_day[room].duration)
        if (start_dur <= start_min or start_dur >= end_min):
            result = {'status': 'OK', 'more': ''}
            return result

        else:
            result = {'status': 'NOK', 'more': 'unavailable hour'}
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
