from django.test import TestCase
from django.urls import reverse, resolve

from search.views import *


class TestUrls(TestCase):

    def test_list(self):
        url = reverse('search:list_voyages')
        self.assertEquals(resolve(url).func.view_class, ListVoyagesView)

    def test_detailed(self):
        url = reverse('search:detailed_voyage', kwargs={'voyage_id': 3})
        self.assertEquals(resolve(url).func.view_class, DetailedVoyageView)
