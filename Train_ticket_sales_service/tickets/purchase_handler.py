from datetime import datetime
import phonenumbers as pn
import logging

from django.db import transaction

from train_main_app.models import Voyage, StationInVoyage, SiteSetting
from Train_ticket_sales_service.settings import general as settings


from .models import PurchasedTicket
from . import utils
from .tasks import *
from .classes import PDFGenerator, EmailSender


class TicketsPurchaseHandler:
    def __init__(self, form_data):

        self.data = dict(form_data)
        self.status_code = 'ok'

    def process_purchase(self, forced_method=None) -> dict:

        if forced_method and forced_method not in settings.PDF_GENERATION_MODES:
            raise AttributeError('Invalid generation method specified. Check PDF_GENERATION_MODES setting.')

        result = {}

        db_ticket_data = self.common_ticket_data()
        voyage = Voyage.objects.select_for_update().get(pk=self.data['voyage_pk'])
        db_ticket_data['voyage'] = voyage

        seat_numbers = tuple(self.data['seat_numbers'].split(','))

        try:
            seats_taken = utils.check_taken_seats(seat_numbers, voyage)
            if seats_taken:
                raise Exception('Seats already taken: '+','.join(seats_taken))

            tickets = self.generate_tickets_and_send_email(seat_numbers, voyage, db_ticket_data.copy(), forced_method)

        except Exception as e:
            logger = logging.getLogger('django')
            logger.error(e)
            self.status_code = 'error'
            result['status'] = self.status_code
            result['ticket_ids'] = []
            return result

        result['status'] = self.status_code
        result['ticket_ids'] = [ticket.pk for ticket in tickets]

        return result

    def common_ticket_data(self):
        ticket_data = {}

        if not self.data['customers_phone_number'] or \
                not isinstance(self.data['customers_phone_number'], pn.PhoneNumber):
            self.data['customers_phone_number'] = pn.PhoneNumber(
                country_code=pn.country_code_for_region(self.data['customers_region_code']),
                national_number=self.data['customers_phone_number']
            )
        pn_object = self.data['customers_phone_number']

        ticket_data['customers_phone_number'] = pn_object.national_number
        ticket_data['customers_region_code'] = pn.region_code_for_country_code(pn_object.country_code)

        ticket_data['departure_station'] = StationInVoyage.objects.get(pk=self.data['departure_en_route_id'])
        ticket_data['arrival_station'] = StationInVoyage.objects.get(pk=self.data['arrival_en_route_id'])

        ticket_data['purchase_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ticket_data['customers_timezone'] = self.data['customers_timezone']

        return ticket_data

    def generate_tickets_and_send_email(
            self, seat_numbers, voyage, ticket_data, forced_method) -> list[PurchasedTicket]:

        with transaction.atomic():
            utils.add_new_taken_seats_to_voyage(seat_numbers, voyage)

            pdf_generation_mode = SiteSetting.get_setting('pdf_generation_mode').value

            if 'realtime' in (pdf_generation_mode, forced_method):
                created_tickets = self.generate_realtime(seat_numbers, ticket_data)

            elif 'async' in (pdf_generation_mode, forced_method):
                created_tickets = self.generate_async(seat_numbers, voyage, ticket_data)

            return created_tickets

    def generate_realtime(self, seat_numbers, ticket_data):

        created_tickets = []

        pdfs = PDFGenerator.generate(utils.simplify_ticket_data(ticket_data.copy()), seat_numbers)

        es = EmailSender()
        es.send_purchased_tickets(self.data['customers_email'], pdfs)

        for seat in seat_numbers:
            pdf_data = pdfs[seat]
            ticket_data['seat_number'] = seat
            ticket_data['pdf_filename'] = pdf_data['filename']

            new_ticket = PurchasedTicket.objects.create(**ticket_data)
            created_tickets.append(new_ticket)

        return created_tickets

    def generate_async(self, seat_numbers, voyage, ticket_data):
        created_tickets = []
        generate_and_send_tickets_task.delay(utils.simplify_ticket_data(ticket_data.copy()), seat_numbers,
                                             voyage.pk, self.data['customers_email'])
        for seat in seat_numbers:
            ticket_data['seat_number'] = seat

            new_ticket = PurchasedTicket.objects.create(**ticket_data)
            created_tickets.append(new_ticket)

        return created_tickets

