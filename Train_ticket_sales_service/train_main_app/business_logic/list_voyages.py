from django.http import Http404
from django.shortcuts import render

from datetime import datetime

from .classes import VoyageFinder
from ..constants import INDEX_FILTER_GET_PARAMETERS
from ..functions import all_keys_exist


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


class ListVoyages:

    def __init__(self, request):
        self.request = request
        self.template_name = 'train_main_app/list_suitable_voyages.html'

    def get(self):
        validate_index_filter_get_parameters(self.request.GET)
        context = self.get_context_data()

        return render(self.request, self.template_name, context)

    def get_context_data(self):
        finder = VoyageFinder(self.request.GET)
        context = {'voyages': finder.find_suitable_voyages()}

        return context

