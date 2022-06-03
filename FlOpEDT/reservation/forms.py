from django.forms import ModelForm
from django import forms
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from reservation.models import *


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ReservationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['has_periodicity'] = forms.BooleanField(required=False,
                                                            initial=False
                                                            )

    class Meta:
        model = Reservation
        fields = '__all__'
        widgets = {
            'date': DateInput(),
            'end': DateInput(),
            'start_time': TimeInput(),
            'end_time': TimeInput()
        }
        labels = {
            'responsible': _("Responsible's name"),
            'room': _("Room"),
            'reservation_type': _('Reservation_type'),
            'title': _("Title of reservation"),
            'description': _("Description"),
            'with_key': _("Borrowed key"),
            'email': _("Send confirmation email"),
            'date': _("Date"),
            'start_time': _("Start time"),
            'end_time': _("End time"),
            'periodicity': _("Periodicity")
        }


class ReservationPeriodicityForm(ModelForm):
    class Meta:
        model = ReservationPeriodicity
        fields = '__all__'
        widgets = {
            'start': DateInput(),
            'end': DateInput()
        }
        labels = {
            'start': _('Start'),
            'end': _('End'),
            'bw_weekdays': _('By weekdays'),
            'bw_weeks_nb': _('By number of week'),
            'bm_x_choice': _('By X of the month'),
            'bm_y_choice': _('By Y of the month')
        }
