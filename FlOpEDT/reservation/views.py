# Create your views here.

from django.forms import ModelForm
from django import forms
from django.shortcuts import render, redirect
from django.db.models import F
from django.template.response import TemplateResponse
from pip._internal import req
from rest_framework.utils import json

from base.models import ScheduledCourse, Week
from base.timing import days_list, time_to_floptime, days_index
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
                if type(save_reservation_result) is Reservation:
                    msg = _('New reservation %s added' % reservation_data['title'])
                    messages.success(request, msg)
                    # The URL and the file location may not be the same after our work,
                    # so I redirect the user in hard to where it should redirect
                    return redirect("reservation:reservationList", department)
                else:
                    return HttpResponse('Reservation impossible : %s' % save_reservation_result['more'])
            else:
                check_periodicity_result = check_periodicity(periodicity_data, reservation_data)
                if check_periodicity_result['status']=='OK':
                    save_periodic_reservations(check_periodicity_result)
                    msg = _('New reservation %s addeds' % check_periodicity_result['ok_reservations'])
                    messages.success(request, msg)
                    # The URL and the file location may not be the same after our work,
                    # so I redirect the user in hard to where it should redirect
                    return redirect("reservation:reservationList", department)
                else:
                    return HttpResponse('Reservations impossibles : %s' % check_periodicity_result['nok_reservations'])
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
    start_time = reservation_data['start_time']
    end_time = reservation_data['end_time']
    start_min = time_to_floptime(start_time)
    end_min = time_to_floptime(end_time)

    #date
    reservation_date = reservation_data['date']
    reservation_day_nb = reservation_date.weekday()
    reservation_day = days_list[reservation_day_nb]
    reservation_year_nb = reservation_date.year
    reservation_week_nb = reservation_date.isocalendar()[1]
    reservation_week = Week.objects.get(nb=reservation_week_nb, year=reservation_year_nb)
    room = reservation_data["room"]

    #filter
    all_room_courses = ScheduledCourse.objects.filter(work_copy=0, room__in=room.and_overrooms())
    same_day_room_scheduled_courses = all_room_courses.filter(day=reservation_day,
                                                              course__week=reservation_week
                                                              )

    simultaneous_room_scheduled_courses = same_day_room_scheduled_courses.filter(start_time__lt=end_min,
                                                                                 start_time__gt=start_min - F('course__type__duration'))
    simultaneous_reservations = Reservation.objects.filter(room=room, date=reservation_date,
                                                           start_time__lt=end_time,
                                                           end_time__gt=start_time)

    if simultaneous_room_scheduled_courses.exists():
        return {'status': 'NOK', 'more': simultaneous_room_scheduled_courses}
    if simultaneous_reservations.exists():
        return {'status': 'NOK', 'more': simultaneous_reservations}

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
                              end_time=reservation_data['end_time'])
        new_res.save()
        return new_res
    else:
        return check

def check_periodicity(periodicity_data, reservation_data):
    result = {'status': 'OK', 'ok_reservations': [], 'nok_reservations': {}, 'periodicity_data':periodicity_data}
    start = periodicity_data["start"]
    end = periodicity_data["end"]
    periodicity_type = periodicity_data["periodicity_type"]
    if periodicity_type == ReservationPeriodicity.PeriodicityType.ByWeek:
        bw_weekdays = periodicity_data["bw_weekdays"]
        bw_weeks_interval = periodicity_data["bw_weeks_interval"]
        bw_integer_weekdays = [days_index[d] for d in bw_weekdays]
        considered_dates = list(rrule(WEEKLY,
                                      dtstart=start,
                                      until=end,
                                      byweekday=bw_integer_weekdays,
                                      interval=bw_weeks_interval))
    elif periodicity_type == ReservationPeriodicity.PeriodicityType.ByMonth:
        bm_x_choice = periodicity_data["bm_x_choice"]
        bm_day_choice = periodicity_data["bm_day_choice"]
        integer_bm_day_choice = days_index[bm_day_choice]
        byweekday_parameter = rrule_days[integer_bm_day_choice](bm_x_choice)
        considered_dates = list(rrule(MONTHLY,
                                      dtstart=start,
                                      until=end,
                                      byweekday=byweekday_parameter))
    else:
        date_nb = start.day
        considered_dates = list(rrule(MONTHLY,
                                      dtstart=start,
                                      until=end,
                                      bymonthday=date_nb))
    for date in considered_dates:
        considered_reservation = reservation_data.copy()
        considered_reservation['date'] = date
        check = check_reservation(considered_reservation)
        if check["status"] == 'OK':
            result['ok_reservations'].append(considered_reservation)
        else:
            result['status']='NOK'
            result['nok_reservations'][considered_reservation] = check['more']
    return result


def save_periodic_reservations(check_periodicity_result):
    periodicity_data = check_periodicity_result["periodicity_data"]
    start = periodicity_data["start"]
    end = periodicity_data["end"]
    periodicity_type = periodicity_data["periodicity_type"]
    periodicity = ReservationPeriodicity(start=start, end=end, periodicity_type=periodicity_type)
    if periodicity_type == ReservationPeriodicity.PeriodicityType.ByWeek:
        periodicity.bw_weekdays = periodicity_data["bw_weekdays"]
        periodicity.bw_weeks_interval = periodicity_data["bw_weeks_interval"]
    elif periodicity_type == ReservationPeriodicity.PeriodicityType.ByMonth:
        periodicity.bm_x_choice = periodicity_data["bm_x_choice"]
        periodicity.bm_day_choice = periodicity_data["bm_day_choice"]
    if check_periodicity_result["status"] == 'OK':
        periodicity.save()
        for reservation in check_periodicity_result['ok_reservations']:
            new_res = save_reservation(reservation)
        new_res.periodicity = periodicity
        new_res.save()
    else:
        pass