import pycountry
from django.utils.text import slugify
from ip2geotools.databases.noncommercial import DbIpCity

from .constants import COUNTRY_NOT_FOUND_VALUE
from .models import SiteSetting


def get_user_ip(meta) -> str:
    x_forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0]
    else:
        user_ip = meta.get('REMOTE_ADDR')

    return user_ip


def get_users_country_or_default(user_ip) -> str:
    default_country = SiteSetting.objects.get(name='default_country')

    try:
        region_code = DbIpCity.get(user_ip, api_key='free').country
        country_name = slugify(pycountry.countries.get(alpha_2=region_code))
    except:
        return default_country.value

    if not SiteSetting.country_available(country_name):
        return default_country.value
    else:
        return country_name




