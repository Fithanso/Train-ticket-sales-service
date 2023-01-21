import json

from train_main_app.functions import split_into_chunks, create_get_parameters


from .constants import SEATS_IN_ROW_IN_WAGONSCHEME


def divide_into_rows_for_display(seats_by_wagons) -> dict:

    # seats should be divided into rows according to the number specified in the constant
    for wagon_name, wagon_info in seats_by_wagons.items():
        wagon_info['seat_numbers'] = split_into_chunks(wagon_info['seat_numbers'], SEATS_IN_ROW_IN_WAGONSCHEME)
    return seats_by_wagons


def link_to_detailed_voyage(voyage, dep_en_route, arr_en_route) -> str:
    get_params_keys = ['departure_en_route', 'arrival_en_route']
    get_params_values = [dep_en_route.pk, arr_en_route.pk]
    return voyage.get_absolute_url() + '?' + create_get_parameters(get_params_keys, get_params_values)
