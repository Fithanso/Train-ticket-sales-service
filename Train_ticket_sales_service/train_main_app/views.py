from urllib.parse import urlencode
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, request, HttpResponseNotFound, Http404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, DetailView, View
from django.forms import *

from urllib.parse import urlencode
import phonenumbers as pn

from .business_logic.classes import *
from .business_logic.list_voyages import ListVoyages
from .forms import *
from .constants import *
from .functions import *
from .business_logic.index_filter import *
from .business_logic.tickets_purchase import *
from .business_logic.detailed_voyage import *
from .models import *


def deni_is_here(request):
    return 'wow it really works'


def index(request):
    return redirect('index_filter', country_name='russia')


def search_purchased_tickets(request):
    handler_object = SearchPurchasedTickets(request)

    if request.method == 'GET':
        return handler_object.get()
    else:
        raise Http404()


def index_filter(request, *args, **kwargs):
    handler_object = IndexFilter(request, kwargs)

    if request.method == 'GET':
        return handler_object.get()
    elif request.method == 'POST':
        return handler_object.post()


def list_voyages(request):
    handler_object = ListVoyages(request)

    if request.method == 'GET':
        return handler_object.get()
    else:
        raise Http404()


def view_voyage(request, *args, **kwargs):

    handler_object = ViewVoyage(request, kwargs)

    if request.method == 'GET':
        return handler_object.get()
    elif request.method == 'POST':
        return handler_object.post()


def purchase_successful(request):
    return render(request, 'train_main_app/purchase_successful.html')



