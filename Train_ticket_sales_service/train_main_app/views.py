from django.views.generic import RedirectView, TemplateView

from tickets.forms import SearchTicketForm

from .forms import VoyagesFilterForm
from .utils import get_user_ip, get_users_country_or_default
from .validators.params_validators import ExistenceValidator
from .models import Country, Station
from .mixins import InvalidParametersRedirectMixin


class RedirectToUsersCountryView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        user_ip = get_user_ip(self.request.META)
        country_name = get_users_country_or_default(user_ip)

        return country_name


class IndexFilterView(TemplateView, InvalidParametersRedirectMixin):
    invalid_parameters_redirect = 'index'

    template_name = 'train_main_app/index_filter.html'
    filter_form = VoyagesFilterForm
    ticket_search_form = SearchTicketForm

    country = None

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
        self.country = Country.objects.get(slug=self.kwargs['country_slug'])

        filter_form, ticket_search_form = self.create_forms()
        context_data['filter_form'] = filter_form
        context_data['ticket_search_form'] = ticket_search_form
        context_data['country_object'] = self.country

        return context_data

    def create_forms(self):
        filter_initial = self.get_filter_initial()

        filter_form = self.filter_form(initial=filter_initial)
        ticket_search_form = self.ticket_search_form()

        return filter_form, ticket_search_form

    def get_filter_initial(self):

        stations = self.get_stations_by_country()

        initial_values = {'departure_station': stations, 'arrival_station': stations,
                          'country': self.kwargs['country_slug']}

        return initial_values

    def get_stations_by_country(self):
        return Station.objects.filter(city__country=self.country)




