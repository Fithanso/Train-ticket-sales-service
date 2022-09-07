from django.http import HttpResponse

from api_funcs.geo_api import get_time_by_address


def api_get_time_by_address(request):
    return HttpResponse(get_time_by_address(request.POST['address']))
