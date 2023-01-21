from django.db.models import QuerySet, Q


from train_main_app.models import Voyage
from train_main_app.display_objects import VoyageDisplayObject


from . import utils


class VoyageFinder:

    def __init__(self, data: dict):

        self.departure_date = data['departure_date']
        self.departure_slug = data['departure_station']
        self.arrival_slug = data['arrival_station']

    def find_suitable_voyages(self) -> list:
        suitable_voyages = []
        voyages_with_suitable_time = self.filter_voyages_by_date()

        for voyage in voyages_with_suitable_time:

            stations_en_route, departure_en_route, arrival_en_route = \
                voyage.get_stations_en_route(self.departure_slug, self.arrival_slug)

            # check if voyage includes stations we need
            if departure_en_route and arrival_en_route:

                # check if stations are in correct order
                if departure_en_route.station_order < arrival_en_route.station_order:

                    # create displaying object of a suitable voyage
                    stations_to_go = arrival_en_route.station_order - departure_en_route.station_order
                    seat_prices = voyage.get_seats_prices(stations_to_go)

                    voyage_link = utils.link_to_detailed_voyage(voyage, departure_en_route, arrival_en_route)

                    suitable_voyage = VoyageDisplayObject(voyage=voyage,
                                                          departure_station=departure_en_route.station,
                                                          arrival_station=arrival_en_route.station,
                                                          stations_en_route=stations_en_route,
                                                          departure_en_route=departure_en_route,
                                                          arrival_en_route=arrival_en_route,
                                                          arrival_datetime=arrival_en_route.arrival_datetime,
                                                          seat_prices=seat_prices,
                                                          link_to_purchase=voyage_link,
                                                          expired=voyage.expired(departure_en_route))

                    suitable_voyages.append(suitable_voyage)

        return suitable_voyages

    def filter_voyages_by_date(self) -> QuerySet:
        return Voyage.objects.filter(Q(departure_datetime__date=self.departure_date))
