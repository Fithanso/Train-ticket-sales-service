from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime


def get_time_by_address(request):
    location = find_location_by_name(request)

    tz_obj = get_tz_by_coordinates(lng=location.longitude, lat=location.latitude)

    time = datetime.now(tz_obj)
    return time.strftime("%H:%M")


def get_tz_by_name(request):
    loc = find_location_by_name(request)
    return get_tz_by_coordinates(lng=loc.longitude, lat=loc.latitude)


def find_location_by_name(loc_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(loc_name)

    return location


def get_tz_by_coordinates(lng, lat):
    tz_finder = TimezoneFinder()
    tz_name = tz_finder.timezone_at(lng=lng, lat=lat)
    tz_obj = pytz.timezone(tz_name)

    return tz_obj
