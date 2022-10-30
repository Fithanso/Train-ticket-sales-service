from django.db import models
import pytz


class PurchasedTicket(models.Model):

    timezones = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    customers_phone_number = models.CharField(max_length=50, verbose_name='Customers phone numebr')
    customers_region_code = models.CharField(max_length=5, default=None, verbose_name='Region code')
    purchase_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Time of purchase')
    customers_timezone = models.CharField(max_length=32, choices=timezones, default='Europe/Moscow')
    voyage = models.ForeignKey('train_main_app.Voyage', on_delete=models.PROTECT, verbose_name='Voyage')
    departure_station = models.ForeignKey('train_main_app.StationInVoyage', on_delete=models.PROTECT,
                                          related_name='departure_st', verbose_name='Departure station')
    arrival_station = models.ForeignKey('train_main_app.StationInVoyage', on_delete=models.PROTECT,
                                        related_name='arrival_st', verbose_name='Arrival station')
    seat_number = models.CharField(max_length=50, verbose_name='Seat number')

    def __str__(self):
        return str(self.customers_phone_number) + " - " + str(self.voyage)

    class Meta:
        db_table = 'purchased_tickets'
        verbose_name = 'Purchased ticket'
        verbose_name_plural = 'Purchased tickets'
        ordering = ['purchase_datetime']

