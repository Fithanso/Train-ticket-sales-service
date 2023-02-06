
from django.core.mail import EmailMessage

from Train_ticket_sales_service.settings import local_fithanso as settings

from . import utils
from .tasks import *


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
        return utils.generate_ticket_pdfs(ticket_data, seat_numbers)


class TicketDisplayObject:

    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

