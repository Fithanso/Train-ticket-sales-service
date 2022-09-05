from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from phonenumber_field.modelfields import PhoneNumberField


class Voyage(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Title')
    train = models.ForeignKey('Train', on_delete=models.PROTECT, verbose_name="Train")
    departure_datetime = models.DateTimeField(verbose_name="Departure time")
    departure_station = models.ForeignKey('Station', on_delete=models.PROTECT, related_name='departure_station',
                                          verbose_name='Departure station')
    arrival_station = models.ForeignKey('Station', on_delete=models.PROTECT, related_name='arrival_station',
                                        verbose_name='Arrival station')

    departure_city = models.ForeignKey('City', on_delete=models.PROTECT, related_name='departure_city',
                                       verbose_name='Departure city')
    arrival_city = models.ForeignKey('City', on_delete=models.PROTECT, related_name='arrival_city',
                                     verbose_name='Arrival city')
    price_per_station = models.IntegerField(blank=True, default=0,
                                            verbose_name="Price per station")

    bc_price_per_station = models.IntegerField(blank=True, default=0,
                                               verbose_name="Price per station for business class")

    taken_seats = models.CharField(max_length=2048, blank=True, verbose_name="Taken seats")

    def __str__(self):
        return self.departure_station.name + ' - ' + self.arrival_station.name

    def get_absolute_url(self):
        return reverse('view_voyage', kwargs={'voyage_id': self.pk})

    class Meta:
        db_table = 'voyages'
        verbose_name = 'Voyage'
        verbose_name_plural = 'Voyages'
        ordering = ['departure_datetime']


class StationInVoyage(models.Model):
    voyage = models.ForeignKey('Voyage', on_delete=models.CASCADE, verbose_name='Voyage')
    station = models.ForeignKey('Station', on_delete=models.CASCADE, verbose_name='Station')
    arrival_datetime = models.DateTimeField(verbose_name='Arrival time')
    station_order = models.PositiveIntegerField(default=0, verbose_name='Station order')

    class Meta:
        db_table = 'stations_in_voyage'
        verbose_name = 'Station in voyage'
        verbose_name_plural = 'Stations in voyage'


class Station(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    name = models.CharField(max_length=255, verbose_name='Name')
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='City')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, verbose_name='Path to image')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'stations'
        verbose_name = 'Station'
        verbose_name_plural = 'Stations'
        ordering = ['name']


class City(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    name = models.CharField(max_length=255, verbose_name='Name')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, verbose_name='Path to image')
    country = models.ForeignKey('Country', on_delete=models.PROTECT, verbose_name='Country')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['name']


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('voyages_filter', kwargs={'country_slug': self.slug})

    class Meta:
        db_table = 'countries'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['name']


class Train(models.Model):
    INCREMENTING_TYPE = 'INCR'

    seats_naming_type_choices = [
        (INCREMENTING_TYPE, 'Incrementing')
    ]

    name = models.CharField(max_length=255, unique=True, verbose_name='Name')

    wagons_number = models.SmallIntegerField(default=0, verbose_name='Wagons q-ty')
    bc_wagons_numbers = models.CharField(max_length=255, default=0, verbose_name='Business Class wagons numbers')

    seats_in_row = models.SmallIntegerField(default=0, verbose_name='Seats in row')
    rows_number = models.SmallIntegerField(default=0, verbose_name='Rows in wagon')
    total_seats = models.SmallIntegerField(default=0, verbose_name='Total seats')
    seats_naming_type = models.CharField(
        max_length=4,
        choices=seats_naming_type_choices,
        default=INCREMENTING_TYPE
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'trains'
        verbose_name = 'Train'
        verbose_name_plural = 'Trains'
        ordering = ['name']


class PurchasedTicket(models.Model):
    customers_phone_number = models.CharField(max_length=50, verbose_name='Customers phone numebr')
    customers_region_code = models.CharField(max_length=5, default=None, verbose_name='Region code')
    purchase_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Time of purchase')
    voyage = models.ForeignKey('Voyage', on_delete=models.PROTECT, verbose_name='Voyage')
    departure_station = models.ForeignKey('StationInVoyage', on_delete=models.PROTECT, related_name='departure_st',
                                          verbose_name='Departure station')
    arrival_station = models.ForeignKey('StationInVoyage', on_delete=models.PROTECT, related_name='arrival_st',
                                        verbose_name='Arrival station')
    seat_number = models.CharField(max_length=50, verbose_name='Seat number')

    def __str__(self):
        return str(self.customers_phone_number) + self.voyage.primary_key

    class Meta:
        db_table = 'purchased_tickets'
        verbose_name = 'Purchased ticket'
        verbose_name_plural = 'Purchased tickets'
        ordering = ['purchase_datetime']


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region_code = models.CharField(max_length=5, default=None, verbose_name='Region code')
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, verbose_name='Phone number')

    def __str__(self):
        return str(self.phone_number)

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class SiteSetting(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True, verbose_name='Setting name')
    value = models.CharField(max_length=100, blank=False, verbose_name='Setting value')

    def __str__(self):
        return self.value

    class Meta:
        db_table = 'settings'
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'
