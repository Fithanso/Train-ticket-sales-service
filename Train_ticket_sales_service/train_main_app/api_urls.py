from django.urls import path

from api import api_get_time_by_address

urlpatterns = [
    path('get_time_by_address/', api_get_time_by_address, name='api_get_time_by_address')
]
