from django.urls import path

from .views import index, voyages_filter, list_voyages, view_voyage

urlpatterns = [
    path('', index, name='index'),
    path('<country_slug>', voyages_filter, name='voyages_filter'),
    path('voyages/', list_voyages, name='list_voyages'),
    path('voyage/<int:voyage_id>/', view_voyage, name='view_voyage'),
]






