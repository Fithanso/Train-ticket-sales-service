from urllib.parse import urlencode
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, request, HttpResponseNotFound, Http404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, DetailView, View
from django.forms import *

from urllib.parse import urlencode
import phonenumbers

from .business_logic.classes import *
from .forms import *
from .constants import *
from .functions import *
from .business_logic.index_filter import *
from .business_logic.tickets_purchase import *
from .models import *


def deni_is_here(request):
    return 'wow it really works'


def index(request):
    return redirect('index_filter', country_name='russia')


class IndexFilter(FormView, View):
    template_name = 'train_main_app/voyage_filter.html'
    form_class = VoyagesFilterForm

    def get_initial(self):
        initial = super().get_initial()

        stations = self.get_stations_by_country()
        # choices for form
        initial['departure_station'] = stations
        initial['arrival_station'] = stations

        return initial

    def get_stations_by_country(self):
        country_name = self.kwargs['country_name'].lower()
        country = get_object_or_404(Country, slug=country_name)

        return Station.objects.filter(city__country=country)

    def get_context_data(self, **kwargs):
        context = super(IndexFilter, self).get_context_data(**kwargs)
        context['form'].fields['country'].initial = self.kwargs['country_name'].lower()

        return context

    def form_valid(self, form):
        data = dict(form.cleaned_data)
        country = Country.objects.get(slug=data['country'])

        departure_station_slug = Station.objects.filter(city__country=country,
                                                        name=data['departure_station'])[0].slug

        arrival_station_slug = Station.objects.filter(city__country=country,
                                                      name=data['arrival_station'])[0].slug
        get_params = data
        get_params['departure_station'] = departure_station_slug
        get_params['arrival_station'] = arrival_station_slug
        get_params.pop('country')

        get_params = create_get_parameters(data.keys(), data.values())

        url = reverse_path_with_get_params('voyages_list', get_params)
        return redirect(url)


class VoyagesList(ListView):
    model = Voyage

    template_name = 'train_main_app/voyages_list.html'

    context_object_name = 'voyages'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VoyagesList, self).get_context_data(**kwargs)

        if not context['voyages']:
            context = {'message': 'No voyages found :('}

        return context

    def get_queryset(self):
        get_params = self.request.GET

        validate_index_filter_get_parameters(get_params)

        finder = VoyageFinder(get_params)
        return finder.find_suitable_voyages()


class ViewVoyage(DetailView):
    # осталось переделать это
    model = Voyage
    pk_url_kwarg = 'voyage_id'
    template_name = 'train_main_app/view_voyage.html'
    context_object_name = 'voyage'

    def get_context_data(self, **kwargs):
        context = super(ViewVoyage, self).get_context_data(**kwargs)

        departure_st_slug = self.request.GET['departure_station']
        arrival_st_slug = self.request.GET['arrival_station']

        form = PurchaseTicketForm
        form.base_fields['voyage_pk'].initial = context['voyage'].pk
        form.base_fields['departure_station_slug'].initial = departure_st_slug
        form.base_fields['arrival_station_slug'].initial = arrival_st_slug

        context['form'] = form

        context['train'] = context['voyage'].train

        tr_getter = TrainInfoGetter(context['voyage'].train)
        context['seats_by_wagons'] = tr_getter.get_seat_names_by_wagons()

        voyage = VoyageInfoGetter.get_detailed_voyage(context['voyage'], departure_st_slug, arrival_st_slug)
        context['voyage'] = voyage

        return context


def purchase_tickets(request):
    result = {}
    print(request.POST)
    voyage = Voyage.objects.get(pk=request.POST['voyage_pk'])

    country_code = request.POST['customers_phone_number_0']
    phone_number = request.POST['customers_phone_number_1']
    departure_station = Station.objects.get(slug=request.POST['departure_station_slug'])
    arrival_station = Station.objects.get(slug=request.POST['arrival_station_slug'])

    valid = phonenumbers.is_valid_number(phonenumbers.parse(phone_number, country_code))
    if not valid:
        result['message'] = 'Invalid phone number'
        return result

    seat_names = tuple(request.POST['seat_names'].split(','))
    taken_seats = check_if_seats_taken(seat_names, voyage)
    if taken_seats:
        result['message'] = 'Requested seats are already taken: ' + ', '.join(taken_seats)
        return result

    add_taken_seats_to_voyage(seat_names, voyage)

    purchase_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for seat in seat_names:
        PurchasedTicket.objects.create(customers_phone_number=phone_number, customers_country_code=country_code,
                                       purchase_datetime=purchase_datetime, voyage=voyage,
                                       departure_station=departure_station, arrival_station=arrival_station,
                                       seat_number=seat)

    return HttpResponse(valid)

