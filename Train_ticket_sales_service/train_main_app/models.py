from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from phonenumber_field.modelfields import PhoneNumberField


class Voyage(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название')
    train = models.ForeignKey('Train', on_delete=models.PROTECT, verbose_name="Поезд")
    departure_datetime = models.DateTimeField(verbose_name="Время отправления")
    departure_station = models.ForeignKey('Station', on_delete=models.PROTECT, related_name='departure_station',
                                          verbose_name='Станция отправления')
    arrival_station = models.ForeignKey('Station', on_delete=models.PROTECT, related_name='arrival_station',
                                        verbose_name='Станция прибытия')

    departure_city = models.ForeignKey('City', on_delete=models.PROTECT, related_name='departure_city',
                                       verbose_name='Город отправления')
    arrival_city = models.ForeignKey('City', on_delete=models.PROTECT, related_name='arrival_city',
                                     verbose_name='Город прибытия')
    price_per_station = models.IntegerField(blank=True, default=0,
                                            verbose_name="Цена за один переезд (станцию)")

    bc_price_per_station = models.IntegerField(blank=True, default=0,
                                               verbose_name="Цена за один переезд (станцию) для бизнес-класса")

    taken_seats = models.CharField(max_length=2048, blank=True, verbose_name="Занятые места")

    def __str__(self):
        return self.departure_station.name + ' - ' + self.arrival_station.name

    def get_absolute_url(self):
        return reverse('view_voyage', kwargs={'voyage_id': self.pk})

    class Meta:
        db_table = 'voyages'
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['departure_datetime']


class StationInVoyage(models.Model):
    voyage = models.ForeignKey('Voyage', on_delete=models.CASCADE, verbose_name='Маршрут')
    station = models.ForeignKey('Station', on_delete=models.CASCADE, verbose_name='Станция')
    arrival_datetime = models.DateTimeField(verbose_name='Время прибытия')
    station_order = models.PositiveIntegerField(default=0, verbose_name='Порядок следования')

    class Meta:
        db_table = 'stations_in_voyage'
        verbose_name = 'Станция в маршруте'
        verbose_name_plural = 'Станции в маршрутах'


class Station(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    name = models.CharField(max_length=255, verbose_name='Название')
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='Город')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, verbose_name='Путь к фотографии')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'stations'
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'
        ordering = ['name']


class City(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    name = models.CharField(max_length=255, verbose_name='Название')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, verbose_name='Путь к фотографии')
    country = models.ForeignKey('Country', on_delete=models.PROTECT, verbose_name='Страна')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'countries'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']


class Train(models.Model):
    INCREMENTING_TYPE = 'INCR'

    seats_naming_type_choices = [
        (INCREMENTING_TYPE, 'Incrementing')
    ]

    name = models.CharField(max_length=255, unique=True, verbose_name='Название')

    wagons_number = models.SmallIntegerField(default=0, verbose_name='Количество вагонов')
    bc_wagons_numbers = models.CharField(max_length=255, default=0, verbose_name='Номера вагонов бизнес-класса')

    seats_in_row = models.SmallIntegerField(default=0, verbose_name='Мест в ряду')
    rows_number = models.SmallIntegerField(default=0, verbose_name='Количество рядов в вагоне')
    total_seats = models.SmallIntegerField(default=0, verbose_name='Всего мест')
    seats_naming_type = models.CharField(
        max_length=4,
        choices=seats_naming_type_choices,
        default=INCREMENTING_TYPE
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'trains'
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['name']


class PurchasedTicket(models.Model):
    customers_phone_number = models.CharField(max_length=50, verbose_name='Телефон клиента')
    purchase_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время покупки')
    voyage = models.ForeignKey('Voyage', on_delete=models.PROTECT, verbose_name='Маршрут')
    departure_station = models.ForeignKey('Station', on_delete=models.PROTECT, related_name='departure_st',
                                          verbose_name='Станция отправления')
    arrival_station = models.ForeignKey('Station', on_delete=models.PROTECT, related_name='arrival_st',
                                        verbose_name='Станция прибытия')
    seat_number = models.CharField(max_length=50, verbose_name='Место')

    def __str__(self):
        return str(self.customers_phone_number) + self.voyage.primary_key

    class Meta:
        db_table = 'purchased_tickets'
        verbose_name = 'Купленный билет'
        verbose_name_plural = 'Купленные билеты'
        ordering = ['purchase_datetime']


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return str(self.phone_number)

    class Meta:
        db_table = 'customers'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
