from django.core.validators import MaxValueValidator
from django.forms import *
from .models import *


class VoyagesFilterForm(forms.Form):
    departure_station = ModelChoiceField(queryset=Station.objects.all(), label='Станция отправления')
    arrival_station = ModelChoiceField(queryset=Station.objects.all(), label='Станция прибытия')
    departure_date = DateField(label='Время отправления',
                               widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
