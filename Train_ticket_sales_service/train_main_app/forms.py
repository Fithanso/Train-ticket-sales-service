from django.forms import *

from .models import Station
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField


class VoyagesFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        super(forms.Form, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            self.fields['departure_station'].queryset = kwargs['initial']['departure_station']
            self.fields['arrival_station'].queryset = kwargs['initial']['arrival_station']
            self.fields['country'].initial = kwargs['initial']['country']

    country = CharField(max_length=50, widget=HiddenInput())
    departure_station = ModelChoiceField(queryset=Station.objects.none(), to_field_name='slug',
                                         label='Departure station')
    arrival_station = ModelChoiceField(queryset=Station.objects.none(), to_field_name='slug', label='Arrival station')
    departure_date = DateField(label='Departure date',
                               widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))





