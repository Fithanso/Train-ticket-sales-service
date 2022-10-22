from django.http import Http404
from django.shortcuts import render

from phonenumbers.phonenumberutil import country_code_for_region

from train_main_app.business_logic.abstract import ViewHandler
from train_main_app.business_logic.validators.params_validators import KeysExistValidator
from .models import PurchasedTicket
from .constants import *


def search_purchased_tickets(request):
    handler_object = SearchPurchasedTickets(request, redirect_to_if_invalid='index')

    if request.method == 'GET':
        return handler_object.get()
    else:
        raise Http404()


def purchase_successful(request):
    return render(request, 'tickets/purchase_successful.html')


class SearchPurchasedTickets(ViewHandler):
    def __init__(self, request, **kwargs):
        self.request = request
        self.redirect_to_if_invalid = kwargs.get('redirect_to_if_invalid', '')

    def get(self):
        val_result = self.validate_parameters()
        if val_result:
            return val_result

        data = self.get_context_data()
        return render(self.request, 'tickets/view_tickets.html', data)

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


class PurchasedTicketInfoGetter:

    @staticmethod
    def get_customers_phonenumber(ticket):
        country_code = country_code_for_region(ticket.customers_region_code)

        return '+' + str(country_code) + ticket.customers_phone_number
