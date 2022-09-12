import phonenumbers as pn
from django.http import Http404
from django.shortcuts import redirect, render

from ..constants import PHONENUMBER_INPUT_NAMES
from ..functions import create_get_parameters, reverse_path_with_get_parameters
from ..forms import VoyagesFilterForm, SearchTicketForm
from ..models import Station, Country
from .validators.params_validators import ExistenceValidator
from .abstract import ViewHandler


class IndexFilter(ViewHandler):

    def __init__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.redirect_to_if_invalid = kwargs.get('redirect_to_if_invalid', '')
        self.country_slug = kwargs['country_slug'].lower()

        self.template_name = 'train_main_app/voyage_filter.html'
        self.filter_form = VoyagesFilterForm
        self.ticket_search_form = SearchTicketForm

    def get(self):
        val_result = self.validate_parameters()
        if val_result:
            return val_result

        data = self.get_context_data()

        return render(self.request, self.template_name, data)

    def validate_parameters(self):

        if not ExistenceValidator.validate(model=Country, search_data={'slug': self.country_slug, 'available': 1}):
            return super().redirect_if_invalid()

        return False

    def post(self):
        if self.ticket_search_form_submitted():
            return self.handle_ticket_search_form()
        else:
            return self.handle_filter_form()

    def ticket_search_form_submitted(self):
        return any(input_name in self.request.POST for input_name in PHONENUMBER_INPUT_NAMES)

    def handle_ticket_search_form(self):
        ticket_search_form = self.ticket_search_form(self.request.POST)
        if ticket_search_form.is_valid():
            return self.redirect_to_ticket_search_result(ticket_search_form)
        else:
            raise Http404()

    def handle_filter_form(self):
        initial_values = self.get_initial_values()

        filter_form = self.filter_form(self.request.POST, initial=initial_values)
        if filter_form.is_valid():
            return self.redirect_to_voyages_list(filter_form)
        else:
            raise Http404()

    def get_context_data(self):
        context_data = {}

        filter_form, ticket_search_form = self.create_forms()
        context_data['filter_form'] = filter_form
        context_data['ticket_search_form'] = ticket_search_form

        return context_data

    def create_forms(self):
        initial_values = self.get_initial_values()

        filter_form = self.filter_form(initial=initial_values)
        ticket_search_form = self.ticket_search_form()

        return filter_form, ticket_search_form

    def get_initial_values(self):

        stations = self.get_stations_by_country()

        initial_values = {'departure_station': stations, 'arrival_station': stations,
                          'country': self.country_slug}

        return initial_values

    def get_stations_by_country(self):
        country = Country.objects.get(slug=self.country_slug)
        return Station.objects.filter(city__country=country)

    def redirect_to_voyages_list(self, form):
        data = dict(form.cleaned_data)
        country = Country.objects.get(slug=data['country'])

        departure_station_slug = Station.objects.filter(city__country=country,
                                                        name=data['departure_station'])[0].slug

        arrival_station_slug = Station.objects.filter(city__country=country,
                                                      name=data['arrival_station'])[0].slug

        data['departure_station'] = departure_station_slug
        data['arrival_station'] = arrival_station_slug
        data.pop('country')

        get_params = create_get_parameters(data.keys(), data.values())

        url = reverse_path_with_get_parameters('list_voyages', get_params)
        return redirect(url)

    def redirect_to_ticket_search_result(self, form):
        data = dict(form.cleaned_data)

        pn_object = data['customers_phone_number']
        data['country_code'] = pn.region_code_for_country_code(pn_object.country_code)
        data['phone_number'] = pn_object.national_number
        data.pop('customers_phone_number')

        get_params = create_get_parameters(data.keys(), data.values())

        url = reverse_path_with_get_parameters('search_purchased_tickets', get_params)
        return redirect(url)
