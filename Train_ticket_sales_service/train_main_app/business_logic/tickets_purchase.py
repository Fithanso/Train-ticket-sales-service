from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render

import phonenumbers as pn
from datetime import datetime

from ..models import Voyage
from ..functions import *
from ..forms import *


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


class SearchPurchasedTickets:
    def __init__(self, request):
        self.request = request

    def get(self):
        tickets_info = self.search_tickets()
        return render(self.request, 'train_main_app/view_tickets.html', {'tickets': tickets_info})

    def search_tickets(self) -> QuerySet:
        phone_number = self.request.GET['phone_number']
        country_code = self.request.GET['country_code']
        return PurchasedTicket.objects.filter(customers_phone_number=phone_number, customers_country_code=country_code)


class PurchaseTickets:
    def __init__(self, form_data):
        self.data = form_data

    def process_purchase(self):
        object_data = self.create_data_for_ticket()
        
        voyage = Voyage.objects.get(pk=self.data['voyage_pk'])
        object_data.update({'voyage': voyage})

        seat_names = tuple(self.data['seat_names'].split(','))

        add_taken_seats_to_voyage(seat_names, voyage)

        for seat in seat_names:
            object_data['seat_number'] = seat
            PurchasedTicket.objects.create(**object_data)

    def create_data_for_ticket(self):
        object_data = {}
        pn_object = self.data['customers_phone_number']

        object_data['customers_phone_number'] = pn_object.national_number
        object_data['customers_country_code'] = pn.region_code_for_country_code(pn_object.country_code)

        object_data['departure_station'] = Station.objects.get(slug=self.data['departure_station_slug'])
        object_data['arrival_station'] = Station.objects.get(slug=self.data['arrival_station_slug'])

        object_data['purchase_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return object_data

