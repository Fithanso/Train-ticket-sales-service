from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class StationAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'city', 'photo', 'get_html_photo')

    list_display = ('id', 'name', 'city', 'photo')

    list_display_links = ('id', 'name')

    search_fields = ('name', 'city')

    list_filter = ('city',)

    prepopulated_fields = {"slug": ("name", "city")}

    readonly_fields = ('get_html_photo',)

    ordering = ['name']

    def get_html_photo(self, object):
        return mark_safe(f" <img src= '{object.photo.url}' width='70' > ")

    get_html_photo.short_description = 'Миниатюра'


class StationInVoyageAdmin(admin.ModelAdmin):
    fields = ('voyage', 'station', 'arrival_datetime', 'station_order')

    list_display = ('id', 'voyage', 'station', 'arrival_datetime')

    list_display_links = ('id',)

    search_fields = ('voyage', 'station')

    readonly_fields = ('voyage', 'station', 'arrival_datetime', 'station_order')


class StationInVoyageInline(admin.TabularInline):
    model = StationInVoyage


class VoyageAdmin(admin.ModelAdmin):
    # что мы видим на странице редактора
    fields = ('title', 'train', 'departure_city', 'departure_station', 'departure_datetime', 'arrival_city',
              'arrival_station', 'price_per_station', 'bc_price_per_station', 'taken_seats')
    # что видим на странице показа всего
    list_display = ('id', 'departure_city', 'arrival_city', 'departure_station', 'departure_datetime',
                    'arrival_station')

    list_display_links = ('id', 'departure_city')
    # по каким полям можно искать
    search_fields = ('departure_city', 'arrival_city', 'departure_station', 'arrival_station')
    # по каким полям делаем фильтры справа
    list_filter = ('departure_city', 'arrival_city', 'departure_station', 'departure_datetime', 'arrival_station')
    save_on_top = True

    inlines = [StationInVoyageInline]


class CityAdmin(admin.ModelAdmin):
    fields = ('name', 'country', 'slug', 'photo', 'get_html_photo')

    list_display = ('id', 'name', 'country', 'photo', 'get_html_photo')

    list_display_links = ('id', 'name')

    list_filter = ('country', )

    search_fields = ('name',)

    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('get_html_photo', )

    def get_html_photo(self, object):
        return mark_safe(f" <img src= '{object.photo.url}' width='70' > ")

    get_html_photo.short_description = 'Миниатюра'


class CountryAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'available')
    list_display = ('id', 'name', 'slug', 'available')

    list_display_links = ('id', 'name')

    list_editable = ('available',)

    search_fields = ('name', 'slug')

    prepopulated_fields = {'slug': ('name', )}


class TrainAdmin(admin.ModelAdmin):
    fields = ('name', 'wagons_number', 'bc_wagons_numbers', 'seats_in_row', 'rows_number', 'total_seats',
              'seats_naming_type')

    list_display = ('id', 'name')

    list_display_links = ('id', 'name')

    search_fields = ('name',)


class CustomerAdmin(admin.ModelAdmin):
    fields = ('user', 'phone_number')
    list_display = ('id', 'user', 'phone_number')
    list_display_links = ('id',)


class SiteSettingAdmin(admin.ModelAdmin):
    fields = ('name', 'value')
    list_display = ('name', 'value')
    list_display_links = ('name', )
    search_fields = ('name',)


admin.site.register(Voyage, VoyageAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Train, TrainAdmin)
admin.site.register(StationInVoyage, StationInVoyageAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(SiteSetting, SiteSettingAdmin)
