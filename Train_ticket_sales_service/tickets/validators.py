from typing import Optional

from .utils import check_taken_seats
from train_main_app.models import Voyage
from train_main_app.abstract import AbstractSeatsValidator


class NoSeatsSelectedValidator(AbstractSeatsValidator):

    def handle(self, seat_numbers: str, voyage: Voyage) -> Optional[str]:
        if seat_numbers == '':
            error_message = 'Choose your seats'
            return error_message
        else:
            return super(NoSeatsSelectedValidator, self).handle(seat_numbers, voyage)


class SeatsTakenValidator(AbstractSeatsValidator):

    def handle(self, seat_numbers: str, voyage: Voyage) -> Optional[str]:
        seat_numbers = tuple(seat_numbers.split(','))
        seats_taken = check_taken_seats(seat_numbers, voyage)

        if seats_taken:
            error_message = 'Requested seats are already taken: ' + ', '.join(seats_taken)
            return error_message
        else:
            return super(SeatsTakenValidator, self).handle(seat_numbers, voyage)

