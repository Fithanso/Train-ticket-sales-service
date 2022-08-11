from datetime import datetime
from urllib.parse import urlencode

from django.http import Http404

from ..constants import INDEX_FILTER_GET_PARAMETERS
from ..models import *


def sluggify_index_filter(data: dict) -> str:
    result_dict = {'country': data['country'], 'departure_station': data['departure_station'].name,
                   'arrival_station': data['arrival_station'].name, 'departure_date': data['departure_date']}

    return urlencode(result_dict)


def all_keys_exist(data_dict, keys) -> bool:
    return all(key in data_dict for key in keys)


def date_has_valid_format(date_str: str, format_str: str) -> bool:
    try:
        datetime.strptime(date_str, format_str)
    except:
        return False

    return True


def validate_index_filter_get_parameters(data):
    if not all_keys_exist(data, INDEX_FILTER_GET_PARAMETERS):
        raise Http404()
    elif not date_has_valid_format(data['departure_date'], '%Y-%m-%d'):
        raise Http404()





