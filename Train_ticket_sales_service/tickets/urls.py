from django.urls import path

from .views import PurchaseSuccessfulView, SearchPurchasedTicketsView, download_ticket_view

app_name = 'tickets'
urlpatterns = [
    path('', SearchPurchasedTicketsView.as_view(), name='search_purchased_tickets'),
    path('purchase_successful/', PurchaseSuccessfulView.as_view(), name='purchase_successful'),
    path('download_ticket/<str:filename>/', download_ticket_view, name='download_ticket')
]
