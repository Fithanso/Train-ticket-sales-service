from django.views.generic import RedirectView, TemplateView

from tickets.forms import SearchTicketForm

from .forms import VoyagesFilterForm
from .utils import get_user_ip, get_users_country_or_default
from .validators.params_validators import ExistenceValidator
from .models import Country, Station
from .mixins import InvalidParametersRedirect


class RedirectToUsersCountryView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        user_ip = get_user_ip(self.request.META)
        country_name = get_users_country_or_default(user_ip)

        return country_name


class IndexFilterView(TemplateView, InvalidParametersRedirect):
    redirect_to_if_invalid = 'index'

    template_name = 'train_main_app/index_filter.html'
    filter_form = VoyagesFilterForm
    ticket_search_form = SearchTicketForm

    def get(self, request, *args, **kwargs):
        val_result = self.validate_parameters()
        if val_result:
            return val_result

        return super(IndexFilterView, self).get(request, *args, **kwargs)

    def validate_parameters(self):

        if not ExistenceValidator.validate(model=Country, search_data={'slug': self.kwargs['country_slug'],
                                                                       'available': 1}):
            return super().redirect_if_invalid()

        return False

    def get_context_data(self, **kwargs):
        context_data = super(IndexFilterView, self).get_context_data(**kwargs)

        filter_form, ticket_search_form = self.create_forms()
        context_data['filter_form'] = filter_form
        context_data['ticket_search_form'] = ticket_search_form
        context_data['country_object'] = Country.objects.get(slug=self.kwargs['country_slug'])

        return context_data

    def create_forms(self):
        initial_values = self.get_initial_values()

        filter_form = self.filter_form(initial=initial_values)
        ticket_search_form = self.ticket_search_form()

        return filter_form, ticket_search_form

    def get_initial_values(self):

        stations = self.get_stations_by_country()

        initial_values = {'departure_station': stations, 'arrival_station': stations,
                          'country': self.kwargs['country_slug']}

        return initial_values

    def get_stations_by_country(self):
        country = Country.objects.get(slug=self.kwargs['country_slug'])
        return Station.objects.filter(city__country=country)



