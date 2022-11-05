from django.views.generic import ListView, TemplateView


import phonenumbers


from train_main_app.validators.params_validators import KeysExistValidator
from train_main_app.mixins import InvalidParametersRedirectMixin

from .models import PurchasedTicket
from .constants import *
from .display_objects import TicketDisplayObject
from . import utils


class PurchaseSuccessfulView(TemplateView):
    template_name = 'tickets/purchase_successful.html'


class SearchPurchasedTicketsView(ListView, InvalidParametersRedirectMixin):
    model = PurchasedTicket
    redirect_to_if_invalid = 'index'
    context_object_name = 'tickets'
    template_name = 'tickets/list_purchased_tickets.html'

    def get(self, request, *args, **kwargs):
        val_result = self.validate_parameters()
        if val_result:
            return val_result

        return super(SearchPurchasedTicketsView, self).get(request, *args, **kwargs)

    def validate_parameters(self):
        if not KeysExistValidator.validate(self.request.GET, SEARCH_TICKETS_GET_PARAMETERS):
            return self.redirect_if_invalid()

    def get_context_data(self, **kwargs):
        context = super(SearchPurchasedTicketsView, self).get_context_data(**kwargs)
        context['tickets'] = self.search_tickets()

        return context

    def search_tickets(self) -> list:

        region_code = self.request.GET['customers_phone_number_0']
        national_number = phonenumbers.parse(self.request.GET['customers_phone_number_1'], region_code).national_number

        detailed_tickets = []

        tickets = PurchasedTicket.objects.filter(customers_phone_number=national_number,
                                                 customers_region_code=region_code).order_by('-purchase_datetime')

        for ticket in tickets:
            display_object = TicketDisplayObject(ticket=ticket,
                                                 departure_station_name=ticket.departure_station.station.name,
                                                 departure_time=ticket.departure_station.arrival_datetime,
                                                 arrival_station_name=ticket.arrival_station.station.name,
                                                 arrival_time=ticket.arrival_station.arrival_datetime,
                                                 customers_phonenumber=utils.get_customers_phonenumber(ticket),
                                                 customers_timezone=ticket.customers_timezone)

            detailed_tickets.append(display_object)

        return detailed_tickets
