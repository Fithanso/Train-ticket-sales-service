
from django.urls import path, re_path, include

from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'voyages', VoyageViewSet)
router.register(r's_in_voyages', StationInVoyageViewSet)
router.register(r'stations', StationViewSet)
router.register(r'cities', CityViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'trains', TrainViewSet)
router.register(r'purchased_tickets', PurchasedTicketViewSet, basename='purchased_tickets')

app_name = 'rest_api'

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('get_time_by_address/', time_by_address, name='time_by_address')

]

