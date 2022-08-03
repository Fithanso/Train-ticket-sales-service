from urllib.parse import urlencode
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, request, HttpResponseNotFound, Http404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from urllib.parse import urlencode
from django.views.generic import FormView, ListView

from .business_logic.classes import *
from .forms import *
from .constants import *
from .functions import *
from .business_logic.index_filter import *
from .models import *


class IndexFilter(FormView):
    template_name = 'train_main_app/index.html'
    form_class = VoyagesFilterForm

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
        data = self.request.GET

        if not all(key in self.request.GET for key in INDEX_FILTER_GET_PARAMETERS):
            raise Http404()

        time_part = (DB_DATE_TIME_SEPARATOR + ("00" + DB_TIME_SEPARATOR) * DB_NUMBER_OF_TIME_PARTS)[:-1]
        date_with_time = data['departure_date'] + time_part
        voyages_with_suitable_time = Voyage.objects.filter(departure_datetime__gte=date_with_time)
        return VoyageFinder.find_suitable_voyages(voyages_with_suitable_time, data)


