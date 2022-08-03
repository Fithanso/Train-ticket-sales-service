from django.urls import reverse
from urllib.parse import urlencode

from .constants import *
from .models import *


def reverse_path_with_get_params(pathname: str, params: str) -> str:
    url = '{}?{}'.format(reverse(pathname), params)
    return url

