from django.test import TestCase, Client
from django.urls import reverse

from tickets.models import PurchasedTicket
from train_main_app.models import Country


#  python manage.py test tickets.tests --settings=Train_ticket_sales_service.settings.local_fithanso --keepdb


class TestSearch(TestCase):
    fixtures = ['fixtures/stations.json', 'fixtures/cities.json', 'fixtures/trains.json', 'fixtures/voyages.json',
                'fixtures/countries.json', 'fixtures/stations_in_voyage.json', 'fixtures/settings.json',
                'fixtures/purchased_tickets.json']

    def setUp(self):
        self.client = Client()

    def test_tickets_found(self):
        get_parameters = '?customers_phone_number_0=RU&customers_phone_number_1=9037930202'
        link = reverse('tickets:search_purchased_tickets') + get_parameters

        response = self.client.get(link)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('tickets/list_purchased_tickets.html')
        self.assertEquals(response.context['full_number'], '+79037930202')
        self.assertEquals(len(response.context['tickets']), 2)
        self.assertQuerysetEqual(response.context['countries'], Country.objects.filter(id__in=[1, 2, 3]))

        self.assertEquals(response.context['tickets'][0].ticket, PurchasedTicket.objects.get(pk=114))
        self.assertEquals(response.context['tickets'][1].ticket, PurchasedTicket.objects.get(pk=113))

        ticket = response.context['tickets'][0]
        self.assertEquals(ticket.customers_phonenumber, '+79037930202')

        attr_names = ['departure_station_name', 'departure_time', 'arrival_station_name', 'arrival_time',
                      'customers_phonenumber', 'customers_timezone']
        for attr in attr_names:
            self.assertTrue(hasattr(ticket, attr))

    def test_tickets_not_found(self):
        get_parameters = '?customers_phone_number_0=RU&customers_phone_number_1=9037930303'
        link = reverse('tickets:search_purchased_tickets') + get_parameters

        response = self.client.get(link)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('tickets/list_purchased_tickets.html')
        self.assertEquals(len(response.context['tickets']), 0)
        self.assertContains(response, 'No tickets were purchased given this number')
        self.assertQuerysetEqual(response.context['countries'], Country.objects.filter(id__in=[1, 2, 3]))

    def test_wrong_parameters(self):
        get_parameters = '?customers_phone_number_0=ZZ&customers_phone_number_1=qwertyuiop'
        link = reverse('tickets:search_purchased_tickets') + get_parameters

        response = self.client.get(link)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('tickets/list_purchased_tickets.html')
        self.assertEquals(len(response.context['tickets']), 0)
        self.assertContains(response, 'No tickets were purchased given this number')
        self.assertQuerysetEqual(response.context['countries'], Country.objects.filter(id__in=[1, 2, 3]))


class TestPurchaseSuccessful(TestCase):

    def test_purchase_successful(self):
        link = reverse('tickets:purchase_successful')

        response = self.client.get(link)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('tickets/purchase_successful.html')


class TestDownloadTicket(TestCase):

    def test_download_ticket(self):
        link = reverse('tickets:download_ticket', kwargs={'filename': '3_9037930202_63.pdf'})

        response = self.client.get(link)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['Content-Type'], 'application/pdf')
        self.assertTrue(int(response.headers['Content-Length']) > 11000)
        self.assertEquals(response.headers['Content-Disposition'], 'inline; filename="3_9037930202_63.pdf"')

    def test_download_ticket_wrong_filename(self):
        link = reverse('tickets:download_ticket', kwargs={'filename': '123456_9037930202_63.pdf'})

        response = self.client.get(link)

        self.assertEquals(response.status_code, 404)
