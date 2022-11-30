from celery import shared_task
import logging
import time

from .classes import *
from .models import PurchasedTicket


@shared_task
def generate_and_send_tickets_task(ticket_data, seat_numbers, voyage_pk, customers_email):
    try:
        time.sleep(5)
        pdfs = PDFGenerator.generate(ticket_data, seat_numbers)

        for seat in seat_numbers:
            pdf_data = pdfs[seat]
            purchased_ticket = PurchasedTicket.objects.filter(voyage=voyage_pk, seat_number=seat,
                                                              customers_phone_number=
                                                              ticket_data['customers_phone_number'])[0]

            if purchased_ticket:
                purchased_ticket.pdf_filename = pdf_data['filename']
                purchased_ticket.save()
            else:
                logger = logging.getLogger('django')
                logger.warning(f'PDF with name {pdf_data["filename"]} could not be saved')

        es = EmailSender()
        es.send_purchased_tickets(customers_email, pdfs)
    except Exception as e:
        logger = logging.getLogger('django')
        logger.error(e)
