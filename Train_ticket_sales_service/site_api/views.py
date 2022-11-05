from django.http import HttpResponse

from train_main_app.functions import get_time_by_address


def time_by_address(request):
    return HttpResponse(get_time_by_address(request.POST['address']))
