from urllib.parse import urlencode
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, request, HttpResponseNotFound, Http404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from urllib.parse import urlencode
from django.views.generic import FormView, ListView, DetailView, View

from .business_logic.classes import *
from .forms import *
from .constants import *
from .functions import *
from .business_logic.index_filter import *
from .models import *
from django.forms import *


class IndexFilter(FormView, View):
    template_name = 'train_main_app/voyage_filter.html'
    form_class = VoyagesFilterForm

    def get_initial(self):
        initial = super().get_initial()

        stations = self.get_stations_by_country()
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
        get_params = sluggify_index_filter(form.cleaned_data)
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
    model = Voyage
    pk_url_kwarg = 'voyage_id'
    template_name = 'train_main_app/view_voyage.html'
    context_object_name = 'voyage'

    def get_context_data(self, **kwargs):
        context = super(ViewVoyage, self).get_context_data(**kwargs)

        form = PurchaseTicketForm
        form.base_fields['voyage_pk'].initial = context['voyage'].pk
        context['form'] = form

        voyage = VoyageInfoGetter.get_detailed_voyage(context['voyage'])
        context['voyage'] = voyage

        return context


def purchase_tickets(request):
    print(request.POST)
    return HttpResponse('hello')



