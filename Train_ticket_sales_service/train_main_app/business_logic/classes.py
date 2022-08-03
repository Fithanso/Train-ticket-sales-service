from django.shortcuts import get_object_or_404

from ..models import *


class VoyageDisplayObject:
    def __init__(self, **kwargs):
        self.voyage = kwargs['voyage']
        self.stations_en_route = kwargs['stations_en_route']
        self.departure_station = kwargs['departure_station']
        self.arrival_station = kwargs['arrival_station']
        self.arrival_datetime = kwargs['arrival_datetime']

        for seat_price in kwargs['seat_prices']:
            setattr(self, seat_price, kwargs['seat_prices'][seat_price])


class VoyageFinder:
    @staticmethod
    def find_suitable_voyages(voyage_entities: [Voyage], data: dict) -> list:
        suitable_voyages = []
        departure_station = get_object_or_404(Station, name=data['departure_station'])
        arrival_station = get_object_or_404(Station, name=data['arrival_station'])

        for voyage in voyage_entities:

            stations_en_route = StationInVoyage.objects.filter(voyage=voyage).order_by('station_order')
            departure_en_route = stations_en_route.filter(station=departure_station)
            arrival_en_route = stations_en_route.filter(station=arrival_station)

            if departure_en_route.exists() and arrival_en_route.exists():
                departure_en_route = departure_en_route[0]
                arrival_en_route = arrival_en_route[0]

                if departure_en_route.station_order < arrival_en_route.station_order:

                    stations_to_go = arrival_en_route.station_order - departure_en_route.station_order
                    seat_prices = VoyageFinder.get_seats_prices(voyage, stations_to_go)

                    suitable_voyage = VoyageDisplayObject(voyage=voyage,
                                                          stations_en_route=stations_en_route,
                                                          departure_station=departure_station,
                                                          arrival_station=arrival_station,
                                                          arrival_datetime=arrival_en_route.arrival_datetime,
                                                          seat_prices=seat_prices)

                    suitable_voyages.append(suitable_voyage)

        return suitable_voyages

    @staticmethod
    def get_seats_prices(voyage, stations_to_go) -> dict:
        normal_seat_price = int(voyage.price_per_station) * stations_to_go
        bc_seat_price = voyage.bc_price_per_station * stations_to_go
        return {'normal_seat_price': normal_seat_price, 'bc_seat_price': bc_seat_price}


