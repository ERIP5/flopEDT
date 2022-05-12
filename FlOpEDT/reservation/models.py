from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import Room
from django.contrib.postgres.fields import ArrayField

from django.utils.translation import gettext_lazy as _


# Create your models here.

class Reservation(models.Model):
    responsible = models.ForeignKey('people.User',  on_delete=models.CASCADE, related_name='reservationResp')
    reservation_type = models.ForeignKey('reservationType', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    key = models.BooleanField()
    reservation_date = models.DateField()
    start = models.PositiveSmallIntegerField()
    duration = models.PositiveIntegerField()
    room = models.ForeignKey('base.Room', on_delete=models.CASCADE, related_name='reservationRoom')
    id_periodicite = models.ForeignKey('ReservationPeriod', on_delete=models.CASCADE, null=True, blank=True)



class ReservationType(models.Model):
    name = models.CharField(max_length=30)

class ReservationPeriod(models.Model):
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
    start = models.DateField()
    ending = models.DateField()

class RoomAttribute(models.Model):
    name = models.CharField(max_length=20)
    class AttributeType(models.TextChoices):
        Boolean = 'B', _('Boolean')
        Numeric = 'N', _('Numeric')
        Enum = 'E', _('Enum')
    attribute_type = models.CharField(
        max_length=1,
        choices=AttributeType.choices,
        default=AttributeType.Boolean,
    )
    # enum choice ne doit être remplie que quand attribute_type est 'enum'
    enum_choices = ArrayField(models.CharField(max_length=20), null=True, default=None, blank=True)
