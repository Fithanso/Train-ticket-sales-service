import os
import pdfkit
import random
from phonenumbers.phonenumberutil import country_code_for_region

from django.template.loader import render_to_string
from django.contrib.staticfiles import finders

from train_main_app.functions import *
from train_main_app.models import Voyage

from Train_ticket_sales_service.settings import local_fithanso as settings


def get_customers_phonenumber(ticket):
    country_code = country_code_for_region(ticket.customers_region_code)

    return '+' + str(country_code) + ticket.customers_phone_number


def add_new_taken_seats_to_voyage(seat_numbers: tuple, voyage: Voyage):
    voyage_seats = voyage.taken_seats.split(',')

    # strip existing just in case
    voyage_seats = strip_in_iter(voyage_seats)
    seat_numbers = strip_in_iter(seat_numbers)

    voyage.taken_seats = ','.join(voyage_seats + seat_numbers)
    voyage.save()


def check_taken_seats(seat_numbers: tuple, voyage: Voyage):
    voyage_seats = voyage.taken_seats.split(',')

    voyage_seats = strip_in_iter(voyage_seats)
    seat_numbers = strip_in_iter(seat_numbers)

    intersection = list(set(voyage_seats) & set(seat_numbers))

    return intersection


def generate_ticket_pdfs(ticket_data, seat_numbers) -> dict:
    if type(seat_numbers) in [str, int]:
        seat_numbers = [seat_numbers]

    config = pdfkit.configuration(wkhtmltopdf=settings.PATH_TO_WKHTMLTOPDF_EXE)
    pdf_dir_path = settings.PURCHASED_TICKETS_PDFS_PATH

    needed_css = [finders.find('tickets/css/list_purchased_tickets.css'),
                  finders.find('train_main_app/css/base.css')]

    rendered_pdfs = {}

    for seat in seat_numbers:
        ticket_data['seat_number'] = seat

        filename = get_ticket_pdf_name(ticket_data, seat)
        output_path = pdf_dir_path + filename

        rendered_template = render_to_string('tickets/ticket_pdf_template.html', ticket_data)
        pdf = pdfkit.from_string(rendered_template, css=needed_css, output_path=output_path, configuration=config)

        rendered_pdfs[seat] = {'pdf': pdf, 'filename': filename}

    return rendered_pdfs


def get_ticket_pdf_name(ticket_data, seat_number):

    return '_'.join([
        str(ticket_data['voyage_pk']),
        str(ticket_data['customers_phone_number']),
        str(seat_number)
    ]) + '.pdf'


def simplify_ticket_data(ticket_data):
    """Remove all model objects, leave only necessary data"""
    ticket_data['voyage_info'] = str(ticket_data['voyage'])
    ticket_data['voyage_pk'] = ticket_data['voyage'].pk
    del ticket_data['voyage']

    ticket_data['departure_station_name'] = ticket_data['departure_station'].station.name
    ticket_data['departure_datetime'] = ticket_data['departure_station'].arrival_datetime
    del ticket_data['departure_station']

    ticket_data['arrival_station_name'] = ticket_data['arrival_station'].station.name
    ticket_data['arrival_datetime'] = ticket_data['arrival_station'].arrival_datetime
    del ticket_data['arrival_station']

    return ticket_data
