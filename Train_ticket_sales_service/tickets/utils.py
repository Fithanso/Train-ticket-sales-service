from phonenumbers.phonenumberutil import country_code_for_region

from train_main_app.functions import *
from train_main_app.models import Voyage


def get_customers_phonenumber(ticket):
    country_code = country_code_for_region(ticket.customers_region_code)

    return '+' + str(country_code) + ticket.customers_phone_number


def add_taken_seats_to_voyage(seat_names: tuple, voyage: Voyage):
    voyage_seats = voyage.taken_seats.split(',')

    # strip existing just in case
    voyage_seats = strip_in_iter(voyage_seats)
    seat_names = strip_in_iter(seat_names)

    new_seats = ','.join(voyage_seats + seat_names)

    voyage.taken_seats = new_seats
    voyage.save()


def find_taken_seats(seat_names: tuple, voyage: Voyage):
    voyage_seats = voyage.taken_seats.split(',')

    voyage_seats = strip_in_iter(voyage_seats)
    seat_names = strip_in_iter(seat_names)

    intersection = list(set(voyage_seats) & set(seat_names))

    return intersection