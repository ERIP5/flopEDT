from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import Room

from django.utils.translation import gettext_lazy as _

# Create your models here.

class Reservation(models.Model):
    responsible = models.ForeignKey('people.User',  on_delete=models.CASCADE, related_name='reservationResp')
    reservation_type = models.ForeignKey('reservation_type', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    key = models.BooleanField()
    reservation_date = models.DateField()
    start = models.PositiveSmallIntegerField()
    duration = models.PositiveIntegerField()
    room = models.ForeignKey('base.Room', on_delete=models.CASCADE, related_name='reservationRoom')
    id_periodicite = models.ForeignKey('Reservation_periode', on_delete=models.CASCADE, null=True, blank=True)

class Reservation_type(models.Model):
    name = models.CharField(max_length=30)

class Reservation_periode(models.Model):
    period_type = models.ForeignKey('Period_type', on_delete=models.CASCADE)
    start = models.DateField()
    ending = models.DateField()

class Period_type(models.Model):
    class PeriodType(models.TextChoices):
        EachDay = 'ED', _('Each day')
        EachWeek = 'EW', _('Each week')
        EachMonth = 'EM', _('Each month')
        FirstDayWeek = 'FDW', _('First day of the week  ')

    period_type = models.CharField(
        max_length=3,
        choices=PeriodType.choices,
        default=PeriodType.EachWeek,
    )
