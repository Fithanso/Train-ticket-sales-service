from django.forms import *

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .validators import NoSeatsSelectedValidator, SeatsTakenValidator
from train_main_app.models import Voyage


class PurchaseTicketForm(forms.Form):

    seat_numbers = CharField(max_length=100, required=False, widget=HiddenInput())
    voyage_pk = CharField(max_length=100, required=False, widget=HiddenInput())
    departure_en_route_id = CharField(max_length=100, required=False, widget=HiddenInput())
    arrival_en_route_id = CharField(max_length=100, required=False, widget=HiddenInput())
    customers_timezone = CharField(max_length=50, required=False, widget=HiddenInput())
    customers_phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='RU'), label='Phone number')
    customers_email = EmailField(max_length=100, label='Email')

    def clean(self):
        self.validate_seat_numbers()

        return self.cleaned_data

    def validate_seat_numbers(self):
        voyage = Voyage.objects.get(pk=self.cleaned_data['voyage_pk'])
        seat_numbers = self.cleaned_data['seat_numbers']

        no_seats_handler = NoSeatsSelectedValidator()
        seats_taken_handler = SeatsTakenValidator()
        no_seats_handler.set_next(seats_taken_handler)

        result = no_seats_handler.handle(seat_numbers, voyage)

        if result:
            self.add_error('seat_numbers', result)


class SearchTicketForm(forms.Form):
    customers_phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='RU',
                                                                             attrs={'placeholder': '(xxx) xxx xx-xx'}),
                                              label='Phone number')
