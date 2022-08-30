from django.urls import path

from .views import *

urlpatterns = [
    path('test/', deni_is_here, name='test'),
    path('', index, name='index'),
    path('<country_name>', index_filter, name='index_filter'),
    path('voyages/', list_voyages, name='list_voyages'),
    path('voyage/<int:voyage_id>/', view_voyage, name='view_voyage'),
    path('tickets/', search_purchased_tickets, name='search_purchased_tickets'),
    path('tickets/purchase_successful/', purchase_successful, name='purchase_successful')
]



