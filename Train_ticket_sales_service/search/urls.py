from django.urls import path

from .views import ListVoyagesView, DetailedVoyageView

app_name = 'search'
urlpatterns = [
    path('voyages/', ListVoyagesView.as_view(), name='list_voyages'),
    path('voyages/<int:voyage_id>/', DetailedVoyageView.as_view(), name='view_voyage')
]
