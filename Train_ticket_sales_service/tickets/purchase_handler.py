from datetime import datetime
import phonenumbers as pn
import logging

from django.db import transaction

from train_main_app.models import Voyage, StationInVoyage
from Train_ticket_sales_service.settings import local_fithanso as settings


from .models import PurchasedTicket
from . import utils
from .tasks import *


class TicketsPurchaseHandler:
    def __init__(self, form_data):
        self.data = form_data
        self.status_code = 'ok'

    def process_purchase(self):
        db_ticket_data = self.common_ticket_data()
        voyage = Voyage.objects.select_for_update().get(pk=self.data['voyage_pk'])
        db_ticket_data['voyage'] = voyage

        seat_numbers = tuple(self.data['seat_numbers'].split(','))

        seats_taken = utils.check_taken_seats(seat_numbers, voyage)
        if seats_taken:
            self.status_code = 'error'
            return self.status_code

        try:
            self.generate_tickets_and_send_email(seat_numbers, voyage, db_ticket_data.copy())

        except Exception as e:
            logger = logging.getLogger('django')
            logger.error(e)
            self.status_code = 'error'

        return self.status_code

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

    def generate_tickets_and_send_email(self, seat_numbers, voyage, ticket_data):

        with transaction.atomic():
            utils.add_new_taken_seats_to_voyage(seat_numbers, voyage)

            if settings.PDF_GENERATION_MODE == 'realtime':

                pdfs = PDFGenerator.generate(utils.simplify_ticket_data(ticket_data.copy()), seat_numbers)

                es = EmailSender()
                es.send_purchased_tickets(self.data['customers_email'], pdfs)

                for seat in seat_numbers:
                    pdf_data = pdfs[seat]
                    ticket_data['seat_number'] = seat
                    ticket_data['pdf_filename'] = pdf_data['filename']

                    PurchasedTicket.objects.create(**ticket_data)

            elif settings.PDF_GENERATION_MODE == 'async':
                generate_and_send_tickets_task.delay(utils.simplify_ticket_data(ticket_data.copy()), seat_numbers,
                                                     voyage.pk, self.data['customers_email'])
                for seat in seat_numbers:
                    ticket_data['seat_number'] = seat

                    PurchasedTicket.objects.create(**ticket_data)
