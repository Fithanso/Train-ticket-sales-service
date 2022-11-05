from django.contrib import admin

from .models import *


class PurchasedTicketAdmin(admin.ModelAdmin):
    fields = ('voyage', 'customers_phone_number', 'purchase_datetime', 'departure_station', 'arrival_station',
              'seat_number')
    list_display = ('id', 'voyage', 'customers_phone_number', 'purchase_datetime', 'departure_station',
                    'arrival_station', 'seat_number')
    list_display_links = ('id',)

    search_fields = ('voyage', 'customers_phone_number', 'departure_station', 'arrival_station')

    list_filter = ('departure_station', 'purchase_datetime', 'arrival_station')

    readonly_fields = ('purchase_datetime',)


admin.site.register(PurchasedTicket, PurchasedTicketAdmin)
