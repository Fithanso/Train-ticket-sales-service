from django.urls import path

from .views import PurchaseSuccessfulView, SearchPurchasedTicketsView

app_name = 'tickets'
urlpatterns = [
    path('', SearchPurchasedTicketsView.as_view(), name='search_purchased_tickets'),
    path('purchase_successful/', PurchaseSuccessfulView.as_view(), name='purchase_successful')
]