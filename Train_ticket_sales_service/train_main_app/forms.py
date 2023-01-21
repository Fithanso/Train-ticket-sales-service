from django.forms import *

from .models import Station


class VoyagesFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        super(forms.Form, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            self.fields['departure_station'].queryset = kwargs['initial']['departure_station']
            self.fields['arrival_station'].queryset = kwargs['initial']['arrival_station']

    departure_station = ModelChoiceField(queryset=Station.objects.none(), to_field_name='slug',
                                         label='Departure station')
    arrival_station = ModelChoiceField(queryset=Station.objects.none(), to_field_name='slug', label='Arrival station')
    departure_date = DateField(label='Departure date',
                               widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))





