from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexFilter.as_view(), name='index_filter'),
    path('voyages/', VoyagesList.as_view(), name='voyages_list'),
    path('voyage/<int:voyage_id>/', ViewVoyage.as_view(), name='view_voyage')
]



