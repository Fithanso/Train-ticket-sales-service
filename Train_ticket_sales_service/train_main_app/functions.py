import pycountry
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from urllib.parse import urlencode
from typing import Iterable
from datetime import datetime


def get_time_by_address(request):
    location = find_location_by_name(request)

    tz_obj = get_tz_by_coordinates(lng=location.longitude, lat=location.latitude)

    if not tz_obj:
        return 'time unavailable'

    time = datetime.now(tz_obj)
    return time.strftime("%H:%M")


def find_location_by_name(loc_name):
    geolocator = Nominatim(user_agent="geoapiExercises")

    try:
        location = geolocator.geocode(loc_name)
    except GeocoderUnavailable:
        return False

    return location


def get_tz_by_name(request):
    loc = find_location_by_name(request)
    if not loc:
        return False

    return get_tz_by_coordinates(lng=loc.longitude, lat=loc.latitude)


def get_tz_by_coordinates(lng, lat):
    tz_finder = TimezoneFinder()
    tz_name = tz_finder.timezone_at(lng=lng, lat=lat)
    tz_obj = pytz.timezone(tz_name)

    return tz_obj


def create_get_parameters(keys: Iterable, values: Iterable) -> str:
    return urlencode(dict(zip(keys, values)))


def strip_in_iter(iterable: Iterable) -> list:
    result = [i.strip() for i in iterable]

    return result


def all_keys_exist(data_dict, keys) -> bool:
    return all(key in data_dict for key in keys)


def split_into_chunks(lst: list, n) -> list:
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])

    return result
