from django.test import TestCase
from datetime import datetime

from train_main_app.models import StationInVoyage, Voyage

from tickets.utils import *
from tickets.models import PurchasedTicket


class TestUtils(TestCase):
    fixtures = ['fixtures/stations.json', 'fixtures/cities.json', 'fixtures/trains.json', 'fixtures/voyages.json',
                'fixtures/countries.json', 'fixtures/stations_in_voyage.json', 'fixtures/settings.json',
                'fixtures/purchased_tickets.json']

    def setUp(self):
        self.maxDiff = None

    def test_get_customers_phonenumber(self):
        result = get_customers_phonenumber(PurchasedTicket.objects.get(pk=113))
        self.assertEquals(result, '+79037930202')

    def test_simplify_ticket_data(self):
        test_data = {'customers_phone_number': 9037930202, 'customers_region_code': 'RU',
                     'departure_station': StationInVoyage.objects.get(pk=15),
                     'arrival_station': StationInVoyage.objects.get(pk=18), 'purchase_datetime': '2023-01-21 00:39:42',
                     'customers_timezone': 'Europe/Moscow', 'voyage': Voyage.objects.get(pk=3)}

        correct_data = {'customers_phone_number': 9037930202, 'customers_region_code': 'RU',
                        'purchase_datetime': '2023-01-21 00:39:42', 'customers_timezone': 'Europe/Moscow',
                        'voyage_info': 'Leningradskiy railway station - Moskovskiy railway station at 2022-08-31 00:00:00',
                        'voyage_pk': 3, 'departure_station_name': 'Leningradskiy railway station',
                        'departure_datetime': datetime(2022, 8, 31, 0, 0),
                        'arrival_station_name': 'Moskovskiy railway station',
                        'arrival_datetime': datetime(2022, 9, 1, 13, 0)}

        result = simplify_ticket_data(test_data)

        self.assertEquals(result, correct_data)
