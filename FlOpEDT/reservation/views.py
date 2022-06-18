# Create your views here.

from django.forms import ModelForm
from django import forms
from django.shortcuts import render, redirect
from django.db.models import F
from django.template.response import TemplateResponse
from pip._internal import req
from rest_framework.utils import json

from base.models import ScheduledCourse, Week
from base.timing import days_list, time_to_floptime
from django.http import HttpResponse
from core.decorators import tutor_or_superuser_required
from django.contrib import messages

from reservation.forms import ReservationForm, ReservationPeriodicityForm
from reservation.models import ReservationPeriodicity, Reservation

from dateutil.rrule import rrule, MONTHLY, WEEKLY, MO, TU, WE, TH, FR, SA, SU
from datetime import *

from django.utils.translation import gettext_lazy as _

rrule_days = [MO, TU, WE, TH, FR, SA, SU]

@tutor_or_superuser_required
def addReservation(request, department):
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        periodicity_form = ReservationPeriodicityForm(request.POST)
        if reservation_form.is_valid() and periodicity_form.is_valid():
            reservation_data = reservation_form.cleaned_data
            periodicity_data = periodicity_form.cleaned_data
            if not reservation_data['has_periodicity']:
                save_reservation_result = save_reservation(reservation_data)
                if save_reservation_result["status"] == 'OK':
                    msg = _('New reservation %s added' % reservation_data['title'])
                    messages.success(request, msg)
                    # The URL and the file location may not be the same after our work,
                    # so I redirect the user in hard to where it should redirect
                    return redirect("http://localhost:8000/fr/reservation/INFO/listeReserv")
                else:
                    return HttpResponse('Reservation impossible : %s' % save_reservation_result['more'])
            else:
                check_periodicity(periodicity_data, reservation_data)
                #Appel à l'api pour toutes les réservations d'un coup.

        else:
            return render(request, 'reservation/form.html', {'reservation_form': reservation_form,
                                                             'periodicity_form': periodicity_form})
    else:
        reservation_form = ReservationForm()
        periodicity_form = ReservationPeriodicityForm()
        return render(request, 'reservation/form.html', {'reservation_form': reservation_form,
                                                         'periodicity_form': periodicity_form})



def list_reserv(req, department):
    user = req.user
    if (user.is_authenticated):
        if user.is_tutor or user.is_superuser:
            button_add = True
        else:
            button_add = False
    else:
        button_add = False
    context = {'is_tutor': json.dumps(button_add)}
    return TemplateResponse(req, "reservation/listeReserv.html", context)


def check_reservation(reservation_data):
    #convert time field in minute
    start_min = time_to_floptime(reservation_data['start_time'])
    end_min = time_to_floptime(reservation_data['end_time'])

    #date
    reservation_day_nb = reservation_data['date'].weekday()
    reservation_day = days_list[reservation_day_nb]
    reservation_year_nb = reservation_data['date'].year
    reservation_week_nb = reservation_data['date'].isocalendar()[1]
    reservation_week = Week.objects.get(nb=reservation_week_nb, year=reservation_year_nb)

    #filter
    all_room_courses = ScheduledCourse.objects.filter(work_copy=0, room=reservation_data['room'])
    same_day_room_scheduled_courses = all_room_courses.filter(day=reservation_day,
                                                              course__week=reservation_week
                                                              )

    simultaneous_room_scheduled_courses = same_day_room_scheduled_courses.filter(start_time__lt=end_min,
                                                                                 start_time__gt=start_min - F('course__type__duration'))

    if simultaneous_room_scheduled_courses.exists():
        return {'status': 'NOK', 'more': simultaneous_room_scheduled_courses}

    return {'status': 'OK', 'more': ''}


def save_reservation(reservation_data):
    check = check_reservation(reservation_data)
    if check['status'] == 'OK':
        new_res = Reservation.objects.create(responsible=reservation_data['responsible'],
                              room=reservation_data['room'],
                              reservation_type=reservation_data['reservation_type'],
                              title=reservation_data['title'],
                              description=reservation_data['description'],
                              with_key=reservation_data['with_key'],
                              email=reservation_data['email'],
                              date=reservation_data['date'],
                              start_time=reservation_data['start_time'],
                              end_time=reservation_data['end_time'],
                              periodicity=reservation_data['periodicity'])
        new_res.save()
    return check


def check_periodicity(periodicity_data, reservation_data):
    result = {'status': 'OK', 'ok_reservations': [], 'nok_reservations': []}
    considered_reservations = []  # fabriquer la liste des dictionnaires de type reservation_data correspondant à la périodicité demandée
    start = periodicity_data["start"]
    end = periodicity_data["end"]
    periodicity_type = periodicity_data["periodicity_type"]
    if periodicity_type == ReservationPeriodicity.PeriodicityType.ByWeek:
        bw_weekdays = periodicity_data["bw_weekdays"]
        # A transformer en liste d'entiers (lundi = 0)
        bw_weeks_interval = periodicity_data["bw_weeks_interval"]
        considered_dates = list(rrule(WEEKLY,
                                      dtstart=start,
                                      until=end,
                                      byweekday=bw_weekdays,
                                      interval=bw_weeks_interval))
    elif periodicity_type == ReservationPeriodicity.PeriodicityType.ByMonth:
        bm_x_choice = periodicity_data["bm_x_choice"]
        bm_day_choice = periodicity_data["bm_day_choice"]
        byweekday_parameter = rrule_days[bm_day_choice](bm_x_choice)
        considered_dates = list(rrule(MONTHLY,
                                      dtstart=start,
                                      until=end,
                                      byweekday=byweekday_parameter))
    else:
        date_nb = 1
        considered_dates = list(rrule(MONTHLY,
                                      dtstart=start,
                                      until=end,
                                      bymonthday=date_nb))
    print(considered_dates)
    for considered_reservation in considered_reservations:
        reservation_result = check_reservation(considered_reservation)
        # if reservation_result['status'] == 'OK':

    # return result