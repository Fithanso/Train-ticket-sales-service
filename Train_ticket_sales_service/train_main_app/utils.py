import pycountry
from django.utils.text import slugify
from ip2geotools.databases.noncommercial import DbIpCity

from .constants import COUNTRY_NOT_FOUND_VALUE, SEATS_IN_ROW_IN_WAGONSCHEME
from .functions import split_into_chunks
from .models import SiteSetting


def divide_seat_names_into_display_groups(seats_by_wagons):
    for wagon_name, wagon_info in seats_by_wagons.items():
        wagon_info['seat_names'] = split_into_chunks(wagon_info['seat_names'], SEATS_IN_ROW_IN_WAGONSCHEME)

    return seats_by_wagons


def get_user_ip(meta) -> str:
    x_forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0]
    else:
        user_ip = meta.get('REMOTE_ADDR')

    return user_ip


def get_users_country_or_default(user_ip) -> str:
    region_code = DbIpCity.get(user_ip, api_key='free').country
    country_name = slugify(pycountry.countries.get(alpha_2=region_code))

    default_country = SiteSetting.objects.get(name='default_country')

    if not SiteSetting.country_available(country_name) or region_code == COUNTRY_NOT_FOUND_VALUE:
        return default_country.value
    else:
        return default_country.value




