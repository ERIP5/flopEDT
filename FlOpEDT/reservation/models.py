from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import Room
from django.contrib.postgres.fields import ArrayField
from base.timing import Day
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class Reservation(models.Model):
    responsible = models.ForeignKey('people.User',  on_delete=models.CASCADE, related_name='reservationResp')
    room = models.ForeignKey('base.Room', on_delete=models.CASCADE, related_name='reservationRoom')
    reservation_type = models.ForeignKey('ReservationType', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    with_key = models.BooleanField(default=False)
    email = models.BooleanField(default=False)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    periodicity = models.ForeignKey("ReservationPeriodicity", null=True, blank=True, on_delete=models.SET_NULL)


class ReservationType(models.Model):
    name = models.CharField(max_length=30)


class ReservationPeriodicity(models.Model):
    class PeriodicityType(models.TextChoices):
        #EachDay = 'ED', _('Each day')
        ByWeek = 'BW', _('By week')
        EachMonthSameDate = 'EM', _('Each month at the same date')
        ByMonth = 'BM', _('By Month')

    class ByMonthX(models.TextChoices):
        AnteLast = 'AL', _('Ante Last')
        Last = 'L', _('Last')
        First = 'F', _('First')

    periodicity_type = models.CharField(
        max_length=2,
        choices=PeriodicityType.choices,
        default=PeriodicityType.ByWeek,
    )
    start = models.DateField(blank=True)
    end = models.DateField(blank=True)

    ### ByWeek Paramaters ###
    # Jours de la semaine qui doivent être inclus dans la réservation ByWeek
    bw_weekdays = ArrayField(models.CharField(max_length=2,
                                              choices=Day.CHOICES), help_text="m, tu, w, th, f", blank=True, null=True)
    # La réservation ByWeek sera reproduite toutes les n semaines (avec n = bw_weeks_nb)
    bw_weeks_nb = models.PositiveSmallIntegerField(blank=True, null=True)

    ### ByMonth Paramaters ###
    # La réservation ByMonth est tous les Xe Y du mois
    bm_x_choice = models.CharField(max_length=2, choices=ByMonthX.choices, blank=True, null=True)
    bm_y_choice = models.CharField(max_length=2, choices=Day.CHOICES, blank=True, null=True)

