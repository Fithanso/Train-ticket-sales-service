from datetime import datetime
import phonenumbers as pn
from django.core.mail import EmailMessage

from django.db import transaction

from train_main_app.models import Voyage, StationInVoyage
from Train_ticket_sales_service.settings import local_fithanso as settings

from .models import PurchasedTicket
from . import utils


class TicketsPurchaseHandler:
    def __init__(self, form_data):
        self.data = form_data
        self.status_code = 'ok'

    def process_purchase(self):
        ticket_data = self.common_ticket_data()

        voyage = Voyage.objects.select_for_update().get(pk=self.data['voyage_pk'])
        ticket_data['voyage'] = voyage

        seat_numbers = tuple(self.data['seat_numbers'].split(','))

        seats_taken = utils.check_taken_seats(seat_numbers, voyage)
        if seats_taken:
            self.status_code = 'error'
            return self.status_code

        es = EmailSender()

        try:
            with transaction.atomic():
                utils.add_new_taken_seats_to_voyage(seat_numbers, voyage)

                pdfs = PDFGenerator.generate(ticket_data.copy(), seat_numbers)

                es.send_purchased_tickets(self.data['customers_email'], pdfs)

                for seat in seat_numbers:
                    pdf_data = pdfs[seat]
                    ticket_data['seat_number'] = seat
                    ticket_data['pdf_filename'] = pdf_data['filename']

                    PurchasedTicket.objects.create(**ticket_data)
        except:
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


class EmailSender:
    def send_purchased_tickets(self, send_to, pdfs):
        email = EmailMessage(
            subject='Thank you for your purchase!',
            body='You will find your tickets in files attached below.',
            from_email=settings.EMAIL_HOST_USER,
            to=[send_to],
            reply_to=[settings.EMAIL_HOST_USER]
        )

        email = self._attach_pdfs_to_email(email, pdfs)

        email.send()

    def _attach_pdfs_to_email(self, email, pdfs, file_dir=settings.PURCHASED_TICKETS_PDFS_PATH):

        for seat_name, value in pdfs.items():
            email.attach_file(file_dir + value['filename'])

        return email


class PDFGenerator:

    @staticmethod
    def generate(ticket_data, seat_numbers):
        if settings.PDF_GENERATION_MODE == 'realtime':
            return PDFGenerator.generate_realtime(ticket_data, seat_numbers)

    @staticmethod
    def generate_realtime(ticket_data, seat_numbers):
        return utils.generate_ticket_pdfs(ticket_data, seat_numbers)
