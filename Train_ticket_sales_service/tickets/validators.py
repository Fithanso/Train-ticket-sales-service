from typing import Optional

from .utils import find_taken_seats
from train_main_app.models import Voyage
from train_main_app.abstract import AbstractSeatsValidator


class NoSeatsSelectedValidator(AbstractSeatsValidator):

    def handle(self, seat_names: str, voyage: Voyage) -> Optional[str]:
        if seat_names == '':
            error_message = 'Choose your seats'
            return error_message
        else:
            return super(NoSeatsSelectedValidator, self).handle(seat_names, voyage)


class SeatsTakenValidator(AbstractSeatsValidator):

    def handle(self, seat_names: str, voyage: Voyage) -> Optional[str]:
        seat_names = tuple(seat_names.split(','))
        seats_taken = find_taken_seats(seat_names, voyage)

        if seats_taken:
            error_message = 'Requested seats are already taken: ' + ', '.join(seats_taken)
            return error_message
        else:
            return super(SeatsTakenValidator, self).handle(seat_names, voyage)

