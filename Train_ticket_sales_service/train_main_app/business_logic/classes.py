import inspect
from typing import Any, Generator, Iterable

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from ..functions import get_zero_time, create_get_parameters
from ..models import *
from .factories import *


class VoyageDisplayObject:

    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __str__(self):
        if hasattr(self, 'departure_station') and hasattr(self, 'arrival_station'):
            return self.departure_station.name + ' - ' + self.arrival_station.name
        return ''


class VoyageInfoGetter:

    @staticmethod
    def get_detailed_voyage(voyage_entity, departure_st_slug, arrival_st_slug):
        stations_en_route, departure_en_route, arrival_en_route = \
            VoyageInfoGetter.get_stations_en_route(voyage_entity, departure_st_slug, arrival_st_slug)

        stations_to_go = arrival_en_route.station_order - departure_en_route.station_order
        seat_prices = VoyageInfoGetter.get_seats_prices(voyage_entity, stations_to_go)

        detailed_voyage = VoyageDisplayObject(voyage_entity=voyage_entity, stations_en_route=stations_en_route,
                                              departure_en_route=departure_en_route, arrival_en_route=arrival_en_route,
                                              stations_to_go=stations_to_go, seat_prices=seat_prices)

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
                factory = IncrementingSeatNamesCreator(self.train)
                return factory.get_incrementing_seat_names()


class VoyageFinder:

    def __init__(self, data: dict):

        self.departure_date = data['departure_date']
        self.departure_slug = data['departure_station']
        self.arrival_slug = data['arrival_station']
        self.stations_to_go = 0

    def find_suitable_voyages(self) -> list:
        suitable_voyages = []
        voyages_with_suitable_time = self.filter_voyages_by_time()

        for voyage in voyages_with_suitable_time:

            stations_en_route, departure_en_route, arrival_en_route = \
                VoyageInfoGetter.get_stations_en_route(voyage, self.departure_slug, self.arrival_slug)

            if departure_en_route and arrival_en_route:

                if departure_en_route.station_order < arrival_en_route.station_order:
                    self.stations_to_go = arrival_en_route.station_order - departure_en_route.station_order
                    seat_prices = VoyageInfoGetter.get_seats_prices(voyage, self.stations_to_go)

                    voyage_link = self.create_link_to_detail_voyage(voyage)

                    suitable_voyage = VoyageDisplayObject(voyage=voyage,
                                                          departure_station=departure_en_route.station,
                                                          arrival_station=arrival_en_route.station,
                                                          stations_en_route=stations_en_route,
                                                          departure_en_route=departure_en_route,
                                                          arrival_en_route=arrival_en_route,
                                                          arrival_datetime=arrival_en_route.arrival_datetime,
                                                          seat_prices=seat_prices,
                                                          link_to=voyage_link)

                    suitable_voyages.append(suitable_voyage)

        return suitable_voyages

    def create_link_to_detail_voyage(self, voyage):
        get_params_keys = ['departure_station', 'arrival_station']
        get_params_values = [self.departure_slug, self.arrival_slug]
        return voyage.get_absolute_url() + '?' + create_get_parameters(get_params_keys, get_params_values)

    def filter_voyages_by_time(self) -> QuerySet:
        time_part = get_zero_time()
        date_with_time = self.departure_date + time_part
        return Voyage.objects.filter(departure_datetime__gte=date_with_time)
