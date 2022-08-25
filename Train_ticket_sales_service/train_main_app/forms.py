from django.core.validators import MaxValueValidator
from django.db.models import QuerySet
from django.forms import *
from .models import *
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField


class VoyagesFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__()
        super(forms.Form, self).__init__(*args, **kwargs)

        self.fields['departure_station'].queryset = kwargs['initial']['departure_station']
        self.fields['arrival_station'].queryset = kwargs['initial']['arrival_station']

    country = CharField(max_length=50, widget=HiddenInput())
    departure_station = ModelChoiceField(queryset=Station.objects.none(), label='Станция отправления')
    arrival_station = ModelChoiceField(queryset=Station.objects.none(), label='Станция прибытия')
    departure_date = DateField(label='Время отправления',
                               widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))


class PurchaseTicketForm(forms.Form):
    seat_names = CharField(max_length=100, widget=HiddenInput())
    voyage_pk = CharField(max_length=100, widget=HiddenInput())
    departure_station_slug = CharField(max_length=100, widget=HiddenInput())
    arrival_station_slug = CharField(max_length=100, widget=HiddenInput())
    customers_phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='RU'), label='Номер телефона')
    customers_email = EmailField(max_length=100, label='Email')




