from django.test import TestCase
from tickets.forms import PurchaseTicketForm, SearchTicketForm

from phonenumber_field.phonenumber import PhoneNumber


class TestForms(TestCase):
    fixtures = ['fixtures/stations.json', 'fixtures/cities.json', 'fixtures/trains.json', 'fixtures/voyages.json',
                'fixtures/countries.json', 'fixtures/stations_in_voyage.json', 'fixtures/settings.json',
                'fixtures/purchased_tickets.json']

    def test_purchase_form(self):
        form = PurchaseTicketForm(data={
            'seat_numbers': '63, 64',
            'voyage_pk': 3,
            'departure_en_route_id': 15,
            'arrival_en_route_id': 18,
            'customers_timezone': 'Europe/Moscow',
            'customers_phone_number_0': 'RU',
            'customers_phone_number_1': '9037930202',
            'customers_email': 'example@mail.com'
        })
        self.assertTrue(form.is_valid())

    def test_purchase_form_wrong_data(self):
        form = PurchaseTicketForm(data={
            'seat_numbers': '10, 11',
            'voyage_pk': 3,
            'departure_en_route_id': 15,
            'arrival_en_route_id': 18,
            'customers_timezone': 'Europe/Moscow',
            'customers_phone_number_0': 'ZZ',
            'customers_phone_number_1': '11119037930202',
            'customers_email': 'examplemail.com'
        })
        self.assertFalse(form.is_valid())
        self.assertTrue('Requested seats are already taken: 11, 10' in form.errors.as_ul() or
                        'Requested seats are already taken: 10, 11' in form.errors.as_ul())
        self.assertTrue(len(form.errors), 3)
        self.assertEquals(list(form.errors.keys()), ['customers_phone_number', 'customers_email', 'seat_numbers'])

    def test_search_form(self):
        form = SearchTicketForm(data={
            'customers_phone_number_0': 'RU',
            'customers_phone_number_1': '9037930202',
        })
        self.assertTrue(form.is_valid())


