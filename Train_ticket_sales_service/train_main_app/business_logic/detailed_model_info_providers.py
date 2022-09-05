from phonenumbers.phonenumberutil import country_code_for_region

from .display_objects import VoyageDisplayObject
from ..functions import strip_in_iter
from ..models import *


class VoyageInfoGetter:

    @staticmethod
    def get_detailed_voyage(voyage_entity, departure_st_slug, arrival_st_slug):
        stations_en_route, departure_en_route, arrival_en_route = \
            VoyageInfoGetter.get_stations_en_route(voyage_entity, departure_st_slug, arrival_st_slug)

        stations_to_go = arrival_en_route.station_order - departure_en_route.station_order
        seat_prices = VoyageInfoGetter.get_seats_prices(voyage_entity, stations_to_go)
        taken_seats = VoyageInfoGetter.get_taken_seats(voyage_entity)

        detailed_voyage = VoyageDisplayObject(voyage_entity=voyage_entity, stations_en_route=stations_en_route,
                                              departure_en_route=departure_en_route, arrival_en_route=arrival_en_route,
                                              stations_to_go=stations_to_go, seat_prices=seat_prices,
                                              taken_seats=taken_seats)

        return detailed_voyage

    @staticmethod
    def get_stations_en_route(voyage: Voyage, departure_st_slug: str, arrival_st_slug: str) -> tuple:
        stations_en_route = StationInVoyage.objects.filter(voyage=voyage).order_by('station_order')
        departure_en_route = stations_en_route.filter(station__slug=departure_st_slug)
        arrival_en_route = stations_en_route.filter(station__slug=arrival_st_slug)

        return (stations_en_route, departure_en_route[0] if departure_en_route.exists() else None,
                arrival_en_route[0] if arrival_en_route.exists() else None)

    @staticmethod
    def get_seats_prices(voyage: Voyage, stations_to_go=1) -> dict:
        normal_seat_price = int(voyage.price_per_station) * stations_to_go
        bc_seat_price = voyage.bc_price_per_station * stations_to_go
        return {'normal_seat_price': normal_seat_price, 'bc_seat_price': bc_seat_price}

    @staticmethod
    def get_taken_seats(voyage: Voyage) -> list:
        return strip_in_iter(voyage.taken_seats.split(','))


class TrainInfoGetter:

    def __init__(self, train_entity):
        self.train = train_entity

        self.seats_in_wagon = 0

        self.start_seats_count_from = 1
        self.stop_seats_count_on = 0
        self.seats_count_step = 1

        self.start_wagons_count_from = 1
        self.stop_wagons_count_on = 0
        self.wagons_count_step = 1

    def get_seat_names_by_wagons(self) -> dict:
        match self.train.seats_naming_type:

            case 'INCR':
                handler = IncrementingSeatNamesCreator(self.train)
                return handler.get_incrementing_seat_names()


class IncrementingSeatNamesCreator:
    def __init__(self, train_entity):
        self.train = train_entity

        self.seats_in_wagon = 0

        self.start_seats_count_from = 1
        self.stop_seats_count_on = 0
        self.seats_count_step = 1

        self.start_wagons_count_from = 1
        self.stop_wagons_count_on = 0
        self.wagons_count_step = 1

    def get_incrementing_seat_names(self) -> dict:
        self.seats_in_wagon = self.train.total_seats // self.train.wagons_number

        self.__create_data_for_incr_calculation()

        seats_divided_by_wagons = {}

        for wagon_number in self.__get_wagons_iterator():
            wagon_number = str(wagon_number)
            seat_names = [str(seat_name) for seat_name in self.__get_seats_iterator()]

            self.__shift_iteration_indent()

            is_bc = wagon_number in self.train.bc_wagons_numbers
            seats_divided_by_wagons[wagon_number] = {'seat_names': seat_names,
                                                     'is_bc_wagon': is_bc}

        return seats_divided_by_wagons

    def __shift_iteration_indent(self):
        self.start_seats_count_from += self.seats_in_wagon
        self.stop_seats_count_on += self.seats_in_wagon

    def __get_wagons_iterator(self):
        return range(self.start_wagons_count_from, self.stop_wagons_count_on, self.wagons_count_step)

    def __get_seats_iterator(self):
        return range(self.start_seats_count_from, self.stop_seats_count_on, self.seats_count_step)

    def __create_data_for_incr_calculation(self):
        self.stop_seats_count_on = self.seats_in_wagon + self.start_seats_count_from
        self.stop_wagons_count_on = self.train.wagons_number + self.start_wagons_count_from


class PurchasedTicketInfoGetter:

    @staticmethod
    def get_customers_phonenumber(ticket):
        country_code = country_code_for_region(ticket.customers_region_code)

        return '+' + str(country_code) + ticket.customers_phone_number


class SiteSettingInfoGetter:

    @staticmethod
    def get_available_countries():
        return Country.objects.all()

    @staticmethod
    def get_currency_sign():
        return SiteSetting.objects.get(name='currency_sign')

    @staticmethod
    def get_currency_name():
        return SiteSetting.objects.get(name='currency_name')
