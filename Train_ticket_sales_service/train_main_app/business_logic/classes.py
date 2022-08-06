import inspect

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from ..functions import get_zero_time
from ..models import *


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
    def get_detailed_voyage(voyage_entity):

        stations_en_route, departure_en_route, arrival_en_route = VoyageInfoGetter.get_stations_en_route(voyage_entity)

        stations_to_go = arrival_en_route.station_order - departure_en_route.station_order
        seat_prices = VoyageInfoGetter.get_seats_prices(voyage_entity, stations_to_go)

        detailed_voyage = VoyageDisplayObject(voyage_entity=voyage_entity, stations_en_route=stations_en_route,
                                              departure_en_route=departure_en_route, arrival_en_route=arrival_en_route,
                                              stations_to_go=stations_to_go, seat_prices=seat_prices)

        return detailed_voyage

    @staticmethod
    def get_stations_en_route(voyage: Voyage) -> tuple:
        stations_en_route = StationInVoyage.objects.filter(voyage=voyage).order_by('station_order')
        departure_en_route = stations_en_route.filter(station=voyage.departure_station)
        arrival_en_route = stations_en_route.filter(station=voyage.arrival_station)

        return (stations_en_route, departure_en_route[0] if departure_en_route.exists() else None,
                arrival_en_route[0] if arrival_en_route.exists() else None)

    @staticmethod
    def get_seats_prices(voyage: Voyage, stations_to_go=1) -> dict:
        normal_seat_price = int(voyage.price_per_station) * stations_to_go
        bc_seat_price = voyage.bc_price_per_station * stations_to_go
        return {'normal_seat_price': normal_seat_price, 'bc_seat_price': bc_seat_price}


class VoyageFinder:

    def __init__(self, data: dict):

        self.departure_date = data['departure_date']
        self.departure_param = data['departure_station']
        self.arrival_param = data['arrival_station']
        self.departure_station = ''
        self.arrival_station = ''
        self.stations_to_go = 0

    def find_suitable_voyages(self) -> list:
        suitable_voyages = []
        voyages_with_suitable_time = self.filter_voyages_by_time()

        self.departure_station = get_object_or_404(Station, name=self.departure_param)
        self.arrival_station = get_object_or_404(Station, name=self.arrival_param)

        for voyage in voyages_with_suitable_time:

            stations_en_route, departure_en_route, arrival_en_route = VoyageInfoGetter.get_stations_en_route(voyage)

            if departure_en_route and arrival_en_route:

                if departure_en_route.station_order < arrival_en_route.station_order:
                    self.stations_to_go = arrival_en_route.station_order - departure_en_route.station_order
                    seat_prices = VoyageInfoGetter.get_seats_prices(voyage, self.stations_to_go)
                    suitable_voyage = VoyageDisplayObject(voyage=voyage,
                                                          stations_en_route=stations_en_route,
                                                          departure_station=self.departure_station,
                                                          arrival_station=self.arrival_station,
                                                          arrival_datetime=arrival_en_route.arrival_datetime,
                                                          seat_prices=seat_prices)

                    suitable_voyages.append(suitable_voyage)

        return suitable_voyages

    def filter_voyages_by_time(self) -> QuerySet:
        time_part = get_zero_time()
        date_with_time = self.departure_date + time_part
        return Voyage.objects.filter(departure_datetime__gte=date_with_time)
