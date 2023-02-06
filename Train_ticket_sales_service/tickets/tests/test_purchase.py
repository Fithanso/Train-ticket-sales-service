import datetime
import os.path

from django.test import TestCase, Client
from django.core import mail

from tickets.purchase_handler import TicketsPurchaseHandler
from tickets.models import PurchasedTicket

from train_main_app.models import Voyage

from Train_ticket_sales_service.settings import general as settings


class TestPurchase(TestCase):
    fixtures = ['fixtures/stations.json', 'fixtures/cities.json', 'fixtures/trains.json', 'fixtures/voyages.json',
                'fixtures/countries.json', 'fixtures/stations_in_voyage.json', 'fixtures/settings.json',
                'fixtures/purchased_tickets.json']

    def setUp(self):
        self.client = Client()
        self.now = datetime.datetime.now()
        self.voyage_pk = 3
        self.voyage = Voyage.objects.get(pk=self.voyage_pk)

    def test_purchase_successful_realtime(self):
        resulting_taken_seats = ',10,11,12,100,41,42,43,44,45,46,47,48,81,82,161,162,6,7,8,13,14,5,4,68,61,62,49,50,' \
                                '1,2,15,16,21,22,25,26,27,28,29,30,31,23,24,20,19,32,40,54,166,58,205,206,204,51,52,' \
                                '55,56,38,39,37,36,35,238,239,237,236,119,120,85,86,63,64'
        ticket_data = {'voyage_pk': self.voyage_pk,
                       'departure_en_route_id': '15',
                       'arrival_en_route_id': '18',
                       'seat_numbers': '63,64',
                       'customers_timezone': 'Europe/Moscow',
                       'customers_region_code': 'RU',
                       'customers_phone_number': '9037930202',
                       'customers_email': 'fms160602@gmail.com'}

        ph = TicketsPurchaseHandler(ticket_data.copy())
        result = ph.process_purchase(forced_method='realtime')

        self.assertEquals(result['status'], 'ok')
        self.assertEquals(result['ticket_ids'], [115, 116])

        p_tickets = list(PurchasedTicket.objects.all())
        self.assertEquals(len(p_tickets), 4)
        self.assertEquals(p_tickets[-2].seat_number, '63')
        self.assertEquals(p_tickets[-1].seat_number, '64')
        p_ticket = p_tickets[-1]

        self.assertEquals(p_ticket.customers_phone_number, ticket_data['customers_phone_number'])
        self.assertEquals(p_ticket.customers_region_code, 'RU')
        self.assertSequenceEqual([p_ticket.purchase_datetime.year, p_ticket.purchase_datetime.month,
                                  p_ticket.purchase_datetime.day, p_ticket.purchase_datetime.hour],
                                 [self.now.year, self.now.month, self.now.day, self.now.hour])
        self.assertTrue(self.now.min <= p_ticket.purchase_datetime.min <= self.now.min + datetime.timedelta(minutes=5))
        self.assertEquals(p_ticket.customers_timezone, 'Europe/Moscow')
        self.assertEquals(p_ticket.voyage_id, self.voyage_pk)
        self.assertEquals(p_ticket.departure_station_id, 15)
        self.assertEquals(p_ticket.arrival_station_id, 18)
        self.assertEquals(p_ticket.pdf_filename, '3_9037930202_64.pdf')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Thank you for your purchase!')
        self.assertEquals(len(mail.outbox[0].attachments), 2)
        self.assertEquals(Voyage.objects.get(pk=self.voyage_pk).taken_seats, resulting_taken_seats)

    def test_purchase_successful_async(self):
        resulting_taken_seats = ',10,11,12,100,41,42,43,44,45,46,47,48,81,82,161,162,6,7,8,13,14,5,4,68,61,62,49,50,' \
                                '1,2,15,16,21,22,25,26,27,28,29,30,31,23,24,20,19,32,40,54,166,58,205,206,204,51,52,' \
                                '55,56,38,39,37,36,35,238,239,237,236,119,120,85,86,63,64'
        ticket_data = {'voyage_pk': self.voyage_pk,
                       'departure_en_route_id': '15',
                       'arrival_en_route_id': '18',
                       'seat_numbers': '63,64',
                       'customers_timezone': 'Europe/Moscow',
                       'customers_region_code': 'RU',
                       'customers_phone_number': '9037930202',
                       'customers_email': 'fms160602@gmail.com'}

        ph = TicketsPurchaseHandler(ticket_data.copy())
        result = ph.process_purchase(forced_method='async')

        self.assertEquals(result['status'], 'ok')
        self.assertEquals(result['ticket_ids'], [115, 116])

        p_tickets = list(PurchasedTicket.objects.all())
        self.assertEquals(len(p_tickets), 4)
        self.assertEquals(p_tickets[-2].seat_number, '63')
        self.assertEquals(p_tickets[-1].seat_number, '64')
        p_ticket = p_tickets[-1]

        self.assertEquals(p_ticket.customers_phone_number, ticket_data['customers_phone_number'])
        self.assertEquals(p_ticket.customers_region_code, 'RU')
        self.assertSequenceEqual([p_ticket.purchase_datetime.year, p_ticket.purchase_datetime.month,
                                  p_ticket.purchase_datetime.day, p_ticket.purchase_datetime.hour],
                                 [self.now.year, self.now.month, self.now.day, self.now.hour])
        self.assertTrue(self.now.min <= p_ticket.purchase_datetime.min <= self.now.min + datetime.timedelta(minutes=5))
        self.assertEquals(p_ticket.customers_timezone, 'Europe/Moscow')
        self.assertEquals(p_ticket.voyage_id, self.voyage_pk)
        self.assertEquals(p_ticket.departure_station_id, 15)
        self.assertEquals(p_ticket.arrival_station_id, 18)
        self.assertEquals(p_ticket.pdf_filename, '3_9037930202_64.pdf')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Thank you for your purchase!')
        self.assertEquals(len(mail.outbox[0].attachments), 2)

        self.assertEquals(Voyage.objects.get(pk=self.voyage_pk).taken_seats, resulting_taken_seats)

        self.assertTrue(os.path.isfile(settings.PURCHASED_TICKETS_PDFS_PATH + '3_9037930202_63.pdf'))
        self.assertTrue(os.path.isfile(settings.PURCHASED_TICKETS_PDFS_PATH + '3_9037930202_64.pdf'))

    def test_purchase_error_taken_seats(self):
        ticket_data = {'voyage_pk': self.voyage_pk,
                       'departure_en_route_id': '15',
                       'arrival_en_route_id': '18',
                       'seat_numbers': '10,11',
                       'customers_timezone': 'Europe/Moscow',
                       'customers_region_code': 'RU',
                       'customers_phone_number': '9037930202',
                       'customers_email': 'fms160602@gmail.com'}

        ph = TicketsPurchaseHandler(ticket_data.copy())
        result = ph.process_purchase(forced_method='realtime')

        self.assertEquals(result['status'], 'error')
        self.assertEquals(result['ticket_ids'], [])

        p_tickets = list(PurchasedTicket.objects.all())
        self.assertEquals(len(p_tickets), 2)

