from datetime import datetime
import json

from django.test import TestCase, Client
from django.urls import reverse

from train_main_app.models import Voyage, Station, StationInVoyage, Train


#  python manage.py test search.tests --settings=Train_ticket_sales_service.settings.local_fithanso --keepdb


class TestList(TestCase):
    fixtures = ['fixtures/stations.json', 'fixtures/cities.json', 'fixtures/trains.json', 'fixtures/voyages.json',
                'fixtures/countries.json', 'fixtures/stations_in_voyage.json', 'fixtures/settings.json']

    def setUp(self):
        self.client = Client()

    def test_voyages_found(self):

        # test one object thoroughly
        get_parameters_1 = '?departure_station=leningradskiy-railway-station-1&arrival_station=moskovskiy-railway-' \
                           'station-2&departure_date=2022-08-31'
        link = reverse('search:list_voyages') + get_parameters_1
        response = self.client.get(link)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list_voyages.html')
        self.assertEquals(len(response.context['voyages']), 1)

        voyage_instance = Voyage.objects.get(pk=3)
        obj = response.context['voyages'][0]
        self.assertEquals(obj.voyage, voyage_instance)
        self.assertEquals(obj.departure_station, Station.objects.get(pk=1))
        self.assertEquals(obj.arrival_station, Station.objects.get(pk=2))

        self.assertEquals(list(obj.stations_en_route), [StationInVoyage.objects.get(pk=15),
                                                        StationInVoyage.objects.get(pk=16),
                                                        StationInVoyage.objects.get(pk=17),
                                                        StationInVoyage.objects.get(pk=18)])
        self.assertEquals(obj.departure_en_route, StationInVoyage.objects.get(pk=15))
        self.assertEquals(obj.arrival_en_route, StationInVoyage.objects.get(pk=18))
        self.assertEquals(obj.arrival_datetime,  datetime(2022, 9, 1, 13, 0))
        self.assertEquals(obj.seat_prices, {'normal_seat_price': 1650, 'bc_seat_price': 3000})
        self.assertEquals(obj.link_to_purchase, '/search/voyages/3/?departure_en_route=15&arrival_en_route=18')
        self.assertEquals(obj.expired, True)

        # test that only checks that two objects are returned
        get_parameters_2 = '?departure_station=leningradskiy-railway-station-1&arrival_station=moskovskiy-railway-' \
                           'station-2&departure_date=2022-08-05'
        link = reverse('search:list_voyages') + get_parameters_2
        response = self.client.get(link)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list_voyages.html')
        self.assertEquals(len(response.context['voyages']), 2)
        self.assertEquals(response.context['voyages'][0].voyage.pk, 1)
        self.assertEquals(response.context['voyages'][1].voyage.pk, 2)

    def test_voyages_not_found(self):
        get_parameters = '?departure_station=leningradskiy-railway-station-1&arrival_station=moskovskiy-railway-' \
                         'station-2&departure_date=2022-08-30'
        link = reverse('search:list_voyages') + get_parameters
        response = self.client.get(link)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list_voyages.html')
        self.assertEquals(len(response.context['voyages']), 0)
        self.assertContains(response, 'No voyages were found')

    def test_wrong_parameters(self):
        get_parameters = '?departure_station=leningradskiy-railway-station-1&arrival_station=moskovskiy-railway-' \
                         'station-2'
        link = reverse('search:list_voyages') + get_parameters
        response = self.client.get(link)

        self.assertEquals(response.status_code, 302)

        get_parameters = '?leningradskiy-railway-station-1&arrival_station=moskovskiy-railway-' \
                         'station-2&departure_date=2022-08-05'
        link = reverse('search:list_voyages') + get_parameters
        response = self.client.get(link)

        self.assertEquals(response.status_code, 302)

        get_parameters = ''
        link = reverse('search:list_voyages') + get_parameters
        response = self.client.get(link)

        self.assertEquals(response.status_code, 302)


class TestDetailedVoyage(TestCase):
    fixtures = ['fixtures/stations.json', 'fixtures/cities.json', 'fixtures/trains.json', 'fixtures/voyages.json',
                'fixtures/countries.json', 'fixtures/stations_in_voyage.json', 'fixtures/settings.json']

    def setUp(self):
        self.client = Client()
        self.voyage_pk = 3

    def test_wrong_parameters(self):
        get_parameters = '?departure_en_route=15'
        link = reverse('search:detailed_voyage', kwargs={'voyage_id': self.voyage_pk}) + get_parameters
        response = self.client.get(link)

        self.assertEquals(response.status_code, 302)

        get_parameters = '?departure_ival_en_route=18'
        link = reverse('search:detailed_voyage', kwargs={'voyage_id': self.voyage_pk}) + get_parameters
        response = self.client.get(link)

        self.assertEquals(response.status_code, 302)

        get_parameters = '?departure_en_route=15123213&arrival_en_route=11231238'
        link = reverse('search:detailed_voyage', kwargs={'voyage_id': self.voyage_pk}) + get_parameters
        response = self.client.get(link)

        self.assertEquals(response.status_code, 302)

        get_parameters = ''
        link = reverse('search:detailed_voyage', kwargs={'voyage_id': self.voyage_pk}) + get_parameters
        response = self.client.get(link)

        self.assertEquals(response.status_code, 302)

    def test_detailed_voyage(self):
        get_parameters = '?departure_en_route=15&arrival_en_route=18'
        link = reverse('search:detailed_voyage', kwargs={'voyage_id': self.voyage_pk}) + get_parameters
        response = self.client.get(link)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/detailed_voyage.html')

        self.assertEquals(response.context['train'], Train.objects.get(pk=1))
        self.assertEquals(response.context['voyage'].voyage_entity, Voyage.objects.get(pk=3))
        self.assertQuerysetEqual(response.context['voyage'].stations_en_route,
                                 StationInVoyage.objects.filter(id__in=[15, 16, 17, 18]))
        self.assertEquals(response.context['voyage'].departure_en_route, StationInVoyage.objects.get(pk=15))
        self.assertEquals(response.context['voyage'].arrival_en_route, StationInVoyage.objects.get(pk=18))
        self.assertEquals(response.context['voyage'].stations_to_go, 3)
        self.assertEquals(response.context['voyage'].seat_prices, {'normal_seat_price': 1650, 'bc_seat_price': 3000})
        self.assertEquals(response.context['voyage'].expired, True)

        with open('search/tests/complex_test_data.json', 'r') as f:
            json_data = json.load(f)

        self.assertEquals(response.context['voyage'].taken_seats, json_data['voyage_3_taken_seats'])
        self.assertEquals(response.context['seats_by_wagons'], json_data['seats_by_wagons_voyage_3'])





