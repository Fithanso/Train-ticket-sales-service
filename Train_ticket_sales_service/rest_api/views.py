from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import action

from search.classes import VoyageFinder
from tickets.purchase_handler import TicketsPurchaseHandler
from train_main_app.models import Voyage, StationInVoyage, Station, City
from tickets.models import PurchasedTicket

from .serializers import *


class VoyageViewSet(viewsets.ModelViewSet):
    queryset = Voyage.objects.all()
    serializer_class = VoyageSerializer

    @action(methods=['get'], detail=False,
            url_path='search/(?P<departure_station>\d{1,9})/(?P<arrival_station>\d{1,9})/'
                     '(?P<departure_date>\d{4}-\d{2}-\d{2})',
            url_name='search')
    def search_voyages(self, request, departure_station, arrival_station, departure_date):
        departure_station = Station.objects.filter(pk=int(departure_station))
        arrival_station = Station.objects.filter(pk=int(arrival_station))

        if not departure_station or not arrival_station:
            raise NotFound(detail={'response': 'Departure or arrival station does not exist.'})

        finder = VoyageFinder({'departure_station': departure_station[0].slug,
                               'arrival_station': arrival_station[0].slug,
                               'departure_date': departure_date})

        serializer = VoyagesSearchResultSerializer(finder.find_suitable_voyages(), many=True)

        return Response(serializer.data)


class StationInVoyageViewSet(viewsets.ModelViewSet):
    queryset = StationInVoyage.objects.all()
    serializer_class = StationInVoyageSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class PurchasedTicketViewSet(viewsets.ModelViewSet):
    serializer_class = PurchasedTicketSerializer

    def get_queryset(self):

        queryset = PurchasedTicket.objects.all()

        customers_phonenumber = self.request.query_params.get('customers_phonenumber')
        if customers_phonenumber is not None:
            queryset = queryset.filter(customers_phone_number=customers_phonenumber)

        return queryset

    @action(methods=['post'], detail=False, url_path='purchase', url_name='purchase')
    def process_purchase(self, request, *args, **kwargs):
        """ Seat names provided through API are not validated if they exist. """

        serializer = PurchaseOperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        purchase_handler = TicketsPurchaseHandler(request.data)
        created_tickets = purchase_handler.process_purchase(forced_method='realtime')
        if created_tickets == 'error':
            return Response('Error occurred while purchasing. Maybe requested seats are already taken.', status=406)
        elif created_tickets == 'ok':
            return Response('Ok', status=200)

