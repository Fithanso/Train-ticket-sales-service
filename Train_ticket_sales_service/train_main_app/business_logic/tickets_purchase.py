from ..models import Voyage
from ..functions import *


def add_taken_seats_to_voyage(seat_names: tuple, voyage: Voyage):

    voyage_seats = voyage.taken_seats.split(',')

    seat_names = ','.join(seat_names)

    voyage.taken_seats = voyage_seats + seat_names


def check_if_seats_taken(seat_names: tuple, voyage: Voyage):
    voyage_seats = voyage.taken_seats.split(',')

    voyage_seats = strip_in_iter(voyage_seats)
    seat_names = strip_in_iter(seat_names)

    intersection = list(set(voyage_seats) & set(seat_names))

    return intersection
