from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from django.contrib import messages

from train_main_app.functions import get_tz_by_name
from train_main_app.mixins import InvalidParametersRedirectMixin
from train_main_app.models import Voyage, StationInVoyage, Station
from train_main_app.validators.params_validators import KeysExistValidator, DateFormatValidator, ExistenceValidator


from tickets.forms import PurchaseTicketForm
from tickets.classes import TicketsPurchaseHandler

from .utils import divide_into_rows_for_display
from .classes import VoyageFinder
from .constants import VOYAGES_FILTER_GET_PARAMETERS, DETAILED_VOYAGE_GET_PARAMETERS, PURCHASE_ERROR_MESSAGE


class ListVoyagesView(ListView, InvalidParametersRedirectMixin):
    invalid_parameters_redirect = 'index'
    template_name = 'search/list_voyages.html'
    context_object_name = 'voyages'

    def get(self, request, *args, **kwargs):
        val_result = self.validate_parameters()
        if val_result:
            return val_result

        return super(ListVoyagesView, self).get(request, *args, **kwargs)

    def validate_parameters(self):
        get_data = self.request.GET

        if not KeysExistValidator.validate(get_data, VOYAGES_FILTER_GET_PARAMETERS):
            return self.redirect_if_invalid()
        elif not DateFormatValidator.validate(get_data['departure_date'], '%Y-%m-%d'):
            return self.redirect_if_invalid()

        return False

    def get_queryset(self):
        # return empty list, because the actual queryset is obtained in get_context_data because other
        # template variables depend on it
        return []
    
    def get_context_data(self, *, object_list=None, **kwargs):
        
        context_data = super(ListVoyagesView, self).get_context_data(**kwargs)

        finder = VoyageFinder(self.request.GET)
        context_data['voyages'] = finder.find_suitable_voyages()

        if context_data[self.context_object_name]:
            context_data['departure_city'] = Station.objects.get(slug=self.request.GET['departure_station']).city
            context_data['arrival_city'] = Station.objects.get(slug=self.request.GET['arrival_station']).city

        return context_data


class DetailedVoyageView(FormView, InvalidParametersRedirectMixin):
    template_name = 'search/detailed_voyage.html'
    success_url = reverse_lazy('tickets:purchase_successful')
    invalid_parameters_redirect = 'index'
    form_class = PurchaseTicketForm

    voyage_id = 0
    departure_st = None
    arrival_st = None
    voyage = None
    form_data = None

    def dispatch(self, request, *args, **kwargs):

        # data that is used in multiple methods goes to attributes
        self.populate_attributes_with_voyage_info()

        return super(DetailedVoyageView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        purchase_handler = TicketsPurchaseHandler(form.cleaned_data)
        purchase_status = purchase_handler.process_purchase()

        if purchase_status == 'error':
            messages.add_message(self.request, messages.ERROR, PURCHASE_ERROR_MESSAGE)
            return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

        return super(DetailedVoyageView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        val_result = self.validate_parameters()
        if val_result:
            return val_result

        return super(DetailedVoyageView, self).get(request, *args, **kwargs)

    def validate_parameters(self):

        if not KeysExistValidator.validate(self.request.GET, DETAILED_VOYAGE_GET_PARAMETERS):
            return self.redirect_if_invalid()

        val_dict = [{'model': Voyage, 'pk': self.kwargs['voyage_id']},
                    {'model': StationInVoyage, 'pk': self.request.GET['departure_en_route']},
                    {'model': StationInVoyage, 'pk': self.request.GET['arrival_en_route']}]

        for entity_info in val_dict:
            if not ExistenceValidator.validate(model=entity_info['model'], search_data={'pk': entity_info['pk']}):
                return self.redirect_if_invalid()

        return False

    def get_context_data(self, **kwargs):

        context = super(DetailedVoyageView, self).get_context_data(**kwargs)
        context['train'] = self.voyage.train

        context['seats_by_wagons'] = divide_into_rows_for_display(self.voyage.train.get_seat_numbers_by_wagons())

        voyage = self.voyage.for_display(self.departure_st.station.slug, self.arrival_st.station.slug)
        context['voyage'] = voyage

        return context

    def populate_attributes_with_voyage_info(self):

        self.voyage_id = self.kwargs['voyage_id']
        self.voyage = Voyage.objects.get(pk=self.kwargs['voyage_id'])
        self.departure_st = \
            StationInVoyage.objects.filter(pk=self.request.GET['departure_en_route']).select_related('station')[0]

        self.arrival_st = \
            StationInVoyage.objects.filter(pk=self.request.GET['arrival_en_route']).select_related('station')[0]

    def get_initial(self):

        timezone = get_tz_by_name(self.voyage.departure_city.name + ',' + self.voyage.departure_city.country.name)
        initial = {'voyage_pk': self.voyage_id, 'departure_station_slug': self.departure_st.station.slug,
                   'arrival_station_slug': self.arrival_st.station.slug, 'departure_en_route_id': self.departure_st.pk,
                   'arrival_en_route_id': self.arrival_st.pk, 'customers_timezone': timezone}

        return initial
