from django.http import Http404
from django.shortcuts import render

from .business_logic.list_voyages import ListVoyages
from .business_logic.voyages_filter import IndexFilter
from .business_logic.tickets_purchase import SearchPurchasedTickets
from .business_logic.detailed_voyage import ViewVoyage
from .geo_manager import RedirectToUsersCountry


def index(request):
    handler_object = RedirectToUsersCountry(request)

    if request.method == 'GET':
        return handler_object.get()
    else:
        raise Http404()


def search_purchased_tickets(request):
    handler_object = SearchPurchasedTickets(request)

    if request.method == 'GET':
        return handler_object.get()
    else:
        raise Http404()


def voyages_filter(request, *args, **kwargs):
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


