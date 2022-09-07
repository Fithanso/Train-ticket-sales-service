from django.db.models import QuerySet, Q
from django.http import Http404
from django.shortcuts import render

from datetime import datetime

from .detailed_model_info_providers import VoyageInfoGetter
from .display_objects import VoyageDisplayObject
from ..constants import VOYAGES_FILTER_GET_PARAMETERS
from ..functions import all_keys_exist, create_get_parameters
from ..models import Voyage


def date_has_valid_format(date_str: str, format_str: str) -> bool:
    try:
        datetime.strptime(date_str, format_str)
    except:
        return False

    return True


def validate_voyages_filter_get_parameters(data):
    if not all_keys_exist(data, VOYAGES_FILTER_GET_PARAMETERS):
        raise Http404()
    elif not date_has_valid_format(data['departure_date'], '%Y-%m-%d'):
        raise Http404()


class ListVoyages:

    def __init__(self, request):
        self.request = request
        self.template_name = 'train_main_app/list_suitable_voyages.html'

    def get(self):
        validate_voyages_filter_get_parameters(self.request.GET)
        context = self.get_context_data()

        return render(self.request, self.template_name, context)

    def get_context_data(self):
        finder = VoyageFinder(self.request.GET)
        context = {'voyages': finder.find_suitable_voyages()}

        return context


class VoyageFinder:

    def __init__(self, data: dict):

        self.departure_date = data['departure_date']
        self.departure_slug = data['departure_station']
        self.arrival_slug = data['arrival_station']
        self.stations_to_go = 0

    def find_suitable_voyages(self) -> list:
        suitable_voyages = []
        voyages_with_suitable_time = self.filter_voyages_by_date()

        for voyage in voyages_with_suitable_time:

            stations_en_route, departure_en_route, arrival_en_route = \
                VoyageInfoGetter.get_stations_en_route(voyage, self.departure_slug, self.arrival_slug)

            if departure_en_route and arrival_en_route:

                if departure_en_route.station_order < arrival_en_route.station_order:
                    self.stations_to_go = arrival_en_route.station_order - departure_en_route.station_order
                    seat_prices = VoyageInfoGetter.get_seats_prices(voyage, self.stations_to_go)

                    voyage_link = self.create_link_to_detail_voyage(voyage, departure_en_route, arrival_en_route)

                    suitable_voyage = VoyageDisplayObject(voyage=voyage,
                                                          departure_station=departure_en_route.station,
                                                          arrival_station=arrival_en_route.station,
                                                          stations_en_route=stations_en_route,
                                                          departure_en_route=departure_en_route,
                                                          arrival_en_route=arrival_en_route,
                                                          arrival_datetime=arrival_en_route.arrival_datetime,
                                                          seat_prices=seat_prices,
                                                          link_to_purchase=voyage_link)

                    suitable_voyages.append(suitable_voyage)

        return suitable_voyages

    def create_link_to_detail_voyage(self, voyage, dep_en_route, arr_en_route):
        get_params_keys = ['departure_en_route', 'arrival_en_route']
        get_params_values = [dep_en_route.pk, arr_en_route.pk]
        return voyage.get_absolute_url() + '?' + create_get_parameters(get_params_keys, get_params_values)

    def filter_voyages_by_date(self) -> QuerySet:
        return Voyage.objects.filter(Q(departure_datetime__date=self.departure_date))

