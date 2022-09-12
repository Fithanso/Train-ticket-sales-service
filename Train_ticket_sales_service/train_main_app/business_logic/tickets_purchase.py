from typing import Optional

from django.shortcuts import render

import phonenumbers as pn
from datetime import datetime

from .validators.params_validators import KeysExistValidator
from .abstract import AbstractSeatsHandler, ViewHandler
from .detailed_model_info_providers import PurchasedTicketInfoGetter
from ..functions import *
from ..models import PurchasedTicket, StationInVoyage, Voyage
from ..constants import SEARCH_TICKETS_GET_PARAMETERS


def add_taken_seats_to_voyage(seat_names: tuple, voyage: Voyage):
    voyage_seats = voyage.taken_seats.split(',')

    # strip existing just in case
    voyage_seats = strip_in_iter(voyage_seats)
    seat_names = strip_in_iter(seat_names)

    new_seats = ','.join(voyage_seats + seat_names)

    voyage.taken_seats = new_seats
    voyage.save()


def check_if_seats_taken(seat_names: tuple, voyage: Voyage):
    voyage_seats = voyage.taken_seats.split(',')

    voyage_seats = strip_in_iter(voyage_seats)
    seat_names = strip_in_iter(seat_names)

    intersection = list(set(voyage_seats) & set(seat_names))

    return intersection


class SearchPurchasedTickets(ViewHandler):
    def __init__(self, request, **kwargs):
        self.request = request
        self.redirect_to_if_invalid = kwargs.get('redirect_to_if_invalid', '')

    def get(self):
        val_result = self.validate_parameters()
        if val_result:
            return val_result

        data = self.get_context_data()
        return render(self.request, 'train_main_app/view_tickets.html', data)

    def validate_parameters(self):
        if not KeysExistValidator.validate(self.request.GET, SEARCH_TICKETS_GET_PARAMETERS):
            return self.redirect_if_invalid()

    def get_context_data(self):
        data = {'tickets': self.search_tickets()}
        return data

    def search_tickets(self) -> list:

        phone_number = self.request.GET['phone_number']
        country_code = self.request.GET['country_code']

        detailed_tickets = []

        tickets = PurchasedTicket.objects.filter(customers_phone_number=phone_number,
                                                 customers_region_code=country_code).order_by('-purchase_datetime')

        for ticket in tickets:
            details = {'ticket': ticket, 'departure_station_name': ticket.departure_station.station.name,
                       'departure_time': ticket.departure_station.arrival_datetime,
                       'arrival_station_name': ticket.arrival_station.station.name,
                       'arrival_time': ticket.arrival_station.arrival_datetime,
                       'customers_phonenumber': PurchasedTicketInfoGetter.get_customers_phonenumber(ticket),
                       'customers_timezone': ticket.customers_timezone}

            detailed_tickets.append(details)

        return detailed_tickets


class PurchaseTickets:
    def __init__(self, form_data):
        self.data = form_data

    def process_purchase(self):
        object_data = self.create_data_for_ticket()

        voyage = Voyage.objects.get(pk=self.data['voyage_pk'])
        object_data['voyage'] = voyage

        seat_names = tuple(self.data['seat_names'].split(','))

        add_taken_seats_to_voyage(seat_names, voyage)

        for seat in seat_names:
            object_data['seat_number'] = seat
            PurchasedTicket.objects.create(**object_data)

    def create_data_for_ticket(self):
        object_data = {}
        pn_object = self.data['customers_phone_number']

        object_data['customers_phone_number'] = pn_object.national_number
        object_data['customers_region_code'] = pn.region_code_for_country_code(pn_object.country_code)

        object_data['departure_station'] = StationInVoyage.objects.get(pk=self.data['departure_en_route_id'])
        object_data['arrival_station'] = StationInVoyage.objects.get(pk=self.data['arrival_en_route_id'])

        object_data['purchase_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        object_data['customers_timezone'] = self.data['customers_timezone']

        return object_data


class NoSeatsSelectedHandler(AbstractSeatsHandler):

    def handle(self, seat_names: str, voyage: Voyage) -> Optional[str]:
        if seat_names == '':
            error_message = 'Choose your seats'
            return error_message


class SeatsTakenHandler(AbstractSeatsHandler):

    def handle(self, seat_names: str, voyage: Voyage) -> Optional[str]:
        seat_names = tuple(seat_names.split(','))
        seats_taken = check_if_seats_taken(seat_names, voyage)

        if seats_taken:
            error_message = 'Requested seats are already taken: ' + ', '.join(seats_taken)
            return error_message
