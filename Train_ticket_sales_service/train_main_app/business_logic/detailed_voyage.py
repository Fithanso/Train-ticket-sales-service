from django.http import Http404
from django.shortcuts import render, reverse, redirect

from .abstract import ViewHandler
from .detailed_model_info_providers import TrainInfoGetter, VoyageInfoGetter
from .validators.params_validators import ExistenceValidator, KeysExistValidator
from .tickets_purchase import PurchaseTickets
from ..constants import DETAILED_VOYAGE_GET_PARAMETERS
from ..api_funcs.geo_api import get_tz_by_name
from ..forms import PurchaseTicketForm
from ..functions import split_into_chunks
from ..models import Voyage, StationInVoyage


class ViewVoyage(ViewHandler):

    def __init__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.get_params = request.GET
        self.redirect_to_if_invalid = kwargs.get('redirect_to_if_invalid', '')
        self.template_name = 'train_main_app/view_voyage.html'
        self.form_class = PurchaseTicketForm
        self.number_of_seats_in_row = 8

        self.voyage_id = 0
        self.departure_en_route_id = ''
        self.arrival_en_route_id = ''
        self.departure_st_slug = ''
        self.arrival_st_slug = ''
        self.voyage = None
        self.form_data = None

    def get(self):
        val_result = self.validate_parameters()
        if val_result:
            return val_result

        self.voyage = Voyage.objects.get(pk=self.voyage_id)

        self.departure_st_slug = StationInVoyage.objects.get(pk=self.departure_en_route_id).station.slug
        self.arrival_st_slug = StationInVoyage.objects.get(pk=self.arrival_en_route_id).station.slug

        context = self.get_context_data()
        context['form'] = self.create_ticket_form()

        return render(self.request, self.template_name, context)

    def validate_parameters(self):

        if not KeysExistValidator.validate(self.get_params, DETAILED_VOYAGE_GET_PARAMETERS):
            return self.redirect_if_invalid()

        val_dict = [{'model': Voyage, 'pk': self.kwargs['voyage_id']},
                    {'model': StationInVoyage, 'pk': self.get_params['departure_en_route']},
                    {'model': StationInVoyage, 'pk': self.get_params['arrival_en_route']}]

        for entity_info in val_dict:
            if not ExistenceValidator.validate(model=entity_info['model'], search_data={'pk': entity_info['pk']}):
                return self.redirect_if_invalid()

        self.departure_en_route_id = self.get_params['departure_en_route']
        self.arrival_en_route_id = self.get_params['arrival_en_route']
        self.voyage_id = self.kwargs['voyage_id']
        return False

    def get_context_data(self):
        context = {'train': self.voyage.train}

        tr_getter = TrainInfoGetter(self.voyage.train)
        context['seats_by_wagons'] = self.divide_seat_names_into_display_groups(tr_getter.get_seat_names_by_wagons())

        voyage = VoyageInfoGetter.get_detailed_voyage(self.voyage, self.departure_st_slug, self.arrival_st_slug)
        context['voyage'] = voyage

        return context

    def divide_seat_names_into_display_groups(self, seats_by_wagons):

        for wagon_name, wagon_info in seats_by_wagons.items():
            wagon_info['seat_names'] = split_into_chunks(wagon_info['seat_names'], self.number_of_seats_in_row)

        return seats_by_wagons

    def post(self):
        self.form_data = self.request.POST

        self.voyage = Voyage.objects.get(pk=self.form_data['voyage_pk'])
        self.voyage_id = self.voyage.pk

        self.departure_st_slug = self.form_data['departure_station_slug']
        self.arrival_st_slug = self.form_data['arrival_station_slug']

        form = self.form_class(self.request.POST)
        context = self.get_context_data()
        context['form'] = form

        if form.is_valid():
            purchase_handler = PurchaseTickets(form.cleaned_data)
            purchase_handler.process_purchase()
            return redirect(reverse('purchase_successful'))
        else:
            return render(self.request, self.template_name, context)

    def create_ticket_form(self):

        initial = self.get_initial()
        form = self.form_class(initial=initial)

        return form

    def get_initial(self):
        timezone = get_tz_by_name(self.voyage.departure_city.name + ',' + self.voyage.departure_city.country.name)
        initial = {'voyage_pk': self.voyage_id, 'departure_station_slug': self.departure_st_slug,
                   'arrival_station_slug': self.arrival_st_slug, 'departure_en_route_id': self.departure_en_route_id,
                   'arrival_en_route_id': self.arrival_en_route_id, 'customers_timezone': timezone}

        return initial
