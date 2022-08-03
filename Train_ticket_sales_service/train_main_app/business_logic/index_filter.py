from datetime import datetime
from urllib.parse import urlencode

from ..models import *


def sluggify_index_filter(data: dict) -> str:
    result_dict = {'departure_station': data['departure_station'].name, 'arrival_station': data['arrival_station'].name,
                   'departure_date': data['departure_date']}

    return urlencode(result_dict)






