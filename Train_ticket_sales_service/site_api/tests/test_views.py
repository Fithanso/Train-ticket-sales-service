from django.urls import reverse

from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from site_api.views import *

import os.path
import ast

from Train_ticket_sales_service.settings import local_fithanso as settings


#  python manage.py test site_api.tests --settings=Train_ticket_sales_service.settings.local_fithanso --keepdb


class TestVoyageViewSet(APITestCase):
    fixtures = ['fixtures/stations.json', 'fixtures/cities.json', 'fixtures/trains.json', 'fixtures/voyages.json',
                'fixtures/countries.json', 'fixtures/stations_in_voyage.json', 'fixtures/settings.json']

    def test_search_voyages(self):
        client = APIClient()
        response = client.get(
            reverse('site_api:voyage-search', kwargs={'departure_station': '1', 'arrival_station': '2',
                                                      'departure_date': '2022-08-31'}))
        self.assertEquals(response.status_code, 200)

        r_data = response.data[0]
        self.assertEquals(list(dict(r_data).keys()), ['voyage', 'departure_station', 'arrival_station',
                                                      'departure_en_route', 'arrival_en_route',
                                                      'arrival_datetime', 'link_to_purchase', 'expired'])
        self.assertEquals(r_data['voyage']['id'], 3)


class TestPurchasedTicketViewSet(APITestCase):
    fixtures = ['fixtures/stations.json', 'fixtures/cities.json', 'fixtures/trains.json', 'fixtures/voyages.json',
                'fixtures/countries.json', 'fixtures/stations_in_voyage.json', 'fixtures/settings.json',
                'fixtures/purchased_tickets.json', 'fixtures/auth_user.json']

    def test_list_tickets(self):
        client = APIClient()
        response = client.get(reverse('site_api:purchased_tickets-list'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data['results']), 2)

    def test_search_tickets(self):
        client = APIClient()
        customers_phonenumber = '9037930202'
        response = client.get(reverse('site_api:purchased_tickets-list') +
                              f'?customers_phonenumber={customers_phonenumber}')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data['results']), 2)

    def test_purchase_ticket(self):

        client = APIClient()
        client.login(username='root', password='root')
        test_data = {'voyage_pk': '3', 'departure_en_route_id': '15', 'arrival_en_route_id': '18',
                     'seat_numbers': '63,64', 'customers_timezone': 'Europe/Moscow', 'customers_region_code': 'RU',
                     'customers_phone_number': '9037930202', 'customers_email': 'example@gmail.com'}

        response = client.post(reverse('site_api:purchased_tickets-purchase'), test_data, format='json')

        self.assertEquals(response.status_code, 200)
        dict_str = response.content.decode("UTF-8")
        response_data = ast.literal_eval(dict_str)

        self.assertEquals(response_data['status'], 'Ok')
        self.assertEquals(response_data['ticket_ids'], '[115, 116]')

        self.assertTrue(os.path.isfile(settings.PURCHASED_TICKETS_PDFS_PATH + '3_9037930202_63.pdf'))
        self.assertTrue(os.path.isfile(settings.PURCHASED_TICKETS_PDFS_PATH + '3_9037930202_64.pdf'))


