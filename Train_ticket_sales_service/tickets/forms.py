from django.forms import *

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .validators import NoSeatsSelectedValidator, SeatsTakenValidator
from train_main_app.models import Voyage


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
    departure_en_route_id = CharField(max_length=100, required=False, widget=HiddenInput())
    arrival_en_route_id = CharField(max_length=100, required=False, widget=HiddenInput())
    customers_timezone = CharField(max_length=50, required=False, widget=HiddenInput())
    customers_phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='RU'), label='Phone number')
    customers_email = EmailField(max_length=100, label='Email')

    def set_initials(self, kwargs):
        for field_name, value in kwargs['initial'].items():
            if field_name not in self.fields:
                raise Exception('Field does not exist in this form')
            self.fields[field_name].initial = value

    def clean(self):
        self.validate_seat_names()

        return self.cleaned_data

    def validate_seat_names(self):
        voyage = Voyage.objects.get(pk=self.cleaned_data['voyage_pk'])
        seat_names = self.cleaned_data['seat_names']

        no_seats_handler = NoSeatsSelectedValidator()
        seats_taken_handler = SeatsTakenValidator()
        no_seats_handler.set_next(seats_taken_handler)

        result = no_seats_handler.handle(seat_names, voyage)

        if result:
            self.add_error('seat_names', result)


class SearchTicketForm(forms.Form):
    customers_phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='RU',
                                                                             attrs={'placeholder': '(xxx) xxx xx-xx'}),
                                              label='Phone number')
