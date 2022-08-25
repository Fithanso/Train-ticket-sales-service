from django.urls import reverse
from urllib.parse import urlencode
from typing import Iterable


from .constants import *
from .models import *


def create_get_parameters(keys: Iterable, values: Iterable) -> str:

    return urlencode(dict(zip(keys, values)))


def reverse_path_with_get_params(pathname: str, params: str) -> str:
    url = '{}?{}'.format(reverse(pathname), params)
    return url


def get_zero_time() -> str:
    return (DB_DATE_TIME_SEPARATOR + ("00" + DB_TIME_SEPARATOR) * DB_NUMBER_OF_TIME_PARTS)[:-1]


def strip_in_iter(iterable: Iterable) -> list:
    result = [i.strip() for i in iterable]

    return result

