from django.urls import path

from .views import IndexFilterView, RedirectToUsersCountryView

urlpatterns = [
    path('', RedirectToUsersCountryView.as_view(), name='index'),
    path('<country_slug>', IndexFilterView.as_view(), name='voyages_filter'),
]






