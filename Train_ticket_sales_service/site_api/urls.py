from django.urls import path

from .views import time_by_address

app_name = 'site_api'
urlpatterns = [
    path('get_time_by_address/', time_by_address, name='time_by_address')
]
