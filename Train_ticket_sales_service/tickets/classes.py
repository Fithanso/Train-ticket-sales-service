from datetime import datetime
import phonenumbers as pn


from train_main_app.models import Voyage, StationInVoyage


from .models import PurchasedTicket
from . import utils


class TicketsPurchaseHandler:
    def __init__(self, form_data):
        self.data = form_data

    def process_purchase(self):
        ticket_data = self.common_ticket_data()

        voyage = Voyage.objects.get(pk=self.data['voyage_pk'])
        ticket_data['voyage'] = voyage

        seat_names = tuple(self.data['seat_names'].split(','))

        utils.add_new_taken_seats_to_voyage(seat_names, voyage)

        for seat in seat_names:
            ticket_data['seat_number'] = seat
            PurchasedTicket.objects.create(**ticket_data)

    def common_ticket_data(self):
        ticket_data = {}
        pn_object = self.data['customers_phone_number']

        ticket_data['customers_phone_number'] = pn_object.national_number
        ticket_data['customers_region_code'] = pn.region_code_for_country_code(pn_object.country_code)

        ticket_data['departure_station'] = StationInVoyage.objects.get(pk=self.data['departure_en_route_id'])
        ticket_data['arrival_station'] = StationInVoyage.objects.get(pk=self.data['arrival_en_route_id'])

        ticket_data['purchase_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ticket_data['customers_timezone'] = self.data['customers_timezone']

        return ticket_data
