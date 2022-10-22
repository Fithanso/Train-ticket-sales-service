from django.urls import path

from .views import search_purchased_tickets, purchase_successful

urlpatterns = [
    path('', search_purchased_tickets, name='search_purchased_tickets'),
    path('purchase_successful/', purchase_successful, name='purchase_successful')
]
