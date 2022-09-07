from django.urls import path

from .views import index, voyages_filter, list_voyages, view_voyage, search_purchased_tickets, purchase_successful

urlpatterns = [
    path('', index, name='index'),
    path('<country_slug>', voyages_filter, name='voyages_filter'),
    path('voyages/', list_voyages, name='list_voyages'),
    path('voyage/<int:voyage_id>/', view_voyage, name='view_voyage'),
    path('tickets/', search_purchased_tickets, name='search_purchased_tickets'),
    path('tickets/purchase_successful/', purchase_successful, name='purchase_successful')
]



