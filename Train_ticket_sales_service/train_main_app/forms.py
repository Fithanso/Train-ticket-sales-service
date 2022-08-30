from django.core.validators import MaxValueValidator
from django.db.models import QuerySet
from django.forms import *

from .business_logic.tickets_purchase import check_if_seats_taken
from .models import *
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
    departure_station = ModelChoiceField(queryset=Station.objects.none(), label='Станция отправления')
    arrival_station = ModelChoiceField(queryset=Station.objects.none(), label='Станция прибытия')
    departure_date = DateField(label='Время отправления',
                               widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))


class PurchaseTicketForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        super(forms.Form, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.set_initials(kwargs)

    seat_names = CharField(max_length=100, required=False, widget=HiddenInput())
    voyage_pk = CharField(max_length=100, required=False, widget=HiddenInput())
    departure_station_slug = CharField(max_length=100, required=False, widget=HiddenInput())
    arrival_station_slug = CharField(max_length=100, required=False, widget=HiddenInput())
    customers_phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='RU'), label='Номер телефона')
    customers_email = EmailField(max_length=100, label='Email')

    def set_initials(self, kwargs):
        for field_name, value in kwargs['initial'].items():
            if field_name not in self.fields:
                raise Exception('Field does not exist in this form')
            self.fields[field_name].initial = value

    def clean(self):

        voyage = Voyage.objects.get(pk=self.cleaned_data['voyage_pk'])
        seat_names = tuple(self.cleaned_data['seat_names'].split(','))

        seats_taken = check_if_seats_taken(seat_names, voyage)
        if seats_taken:
            error_message = 'Requested seats are already taken: ' + ', '.join(seats_taken)
            self.add_error('seat_names', error_message)

        return self.cleaned_data


class SearchTicketForm(forms.Form):
    customers_phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='RU',
                                                                             attrs={'placeholder': '(xxx) xxx xx-xx'}),
                                              label='Номер телефона')




