from django.urls import path

from .views import *

urlpatterns = [
    path('test/', deni_is_here, name='test'),
    path('', index, name='index'),
    path('<country_name>', IndexFilter.as_view(), name='index_filter'),
    path('voyages/', VoyagesList.as_view(), name='voyages_list'),
    path('voyage/<int:voyage_id>/', ViewVoyage.as_view(), name='view_voyage'),
    path('purchase_tickets/', purchase_tickets, name='purchase_tickets')
]



