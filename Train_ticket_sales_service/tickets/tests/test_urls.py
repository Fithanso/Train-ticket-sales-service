from django.test import TestCase
from django.urls import reverse, resolve

from tickets.views import *


class TestUrls(TestCase):

    def test_search(self):
        url = reverse('tickets:search_purchased_tickets')
        self.assertEquals(resolve(url).func.view_class, SearchPurchasedTicketsView)

    def test_purchase_successful(self):
        url = reverse('tickets:purchase_successful')
        self.assertEquals(resolve(url).func.view_class, PurchaseSuccessfulView)

    def test_download(self):
        url = reverse('tickets:download_ticket', kwargs={'filename': '3_9037930202_63.pdf'})
        self.assertEquals(resolve(url).func, download_ticket_view)
