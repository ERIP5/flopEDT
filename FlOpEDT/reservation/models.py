from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import Room

from django.utils.translation import gettext_lazy as _

# Create your models here.
period_choice= [
    ('each_week', 'Each week'),
    ('each_month', 'Each month'),
    ('each_year', 'Each year'),
    ('XY', 'X Y of the month'),
    ]

each_week_ch =(
    ("1", "Each week"),
    ("2", "Each 2 weeks"),
    ("3", "Each 3 weeks"),
    ("4", "Each 4 weeks"),
)

each_x_ch =(
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("last", "Last"),
)

each_y_ch =(
    ("m", "Monday"),
    ("tu", "Tuesday"),
    ("w", "Wednesday"),
    ("th", "Thursday"),
    ("f", "Friday"),
    ("sa", "Saturday"),
    ("su", "Sunday"),
)

class Reservation(models.Model):
    responsible = models.ForeignKey('people.User',  on_delete=models.CASCADE, related_name='reservationResp')
    room = models.ForeignKey('base.Room', on_delete=models.CASCADE, related_name='reservationRoom')
    reservation_type = models.ForeignKey('reservation_type', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    key = models.BooleanField(default=False)
    courriel = models.BooleanField(default=False)
    reservation_date = models.DateField()
    start = models.PositiveSmallIntegerField()
    duration = models.PositiveIntegerField()
    periodicity = models.BooleanField(default=False)
    Period_choice = models.CharField(max_length=99, help_text="Only required if 'periodicity' is selected ", blank=True, null=True)
    each_week_choice = models.CharField(max_length=99,choices=each_week_ch, blank=True, null=True)
    each_x_choice = models.CharField(max_length=99,choices=each_x_ch, blank=True, null=True)
    each_y_choice = models.CharField(max_length=99,choices=each_y_ch, blank=True, null=True)
    end_period = models.DateField(blank=True, null=True)


class Reservation_type(models.Model):
    name = models.CharField(max_length=30)
