$(document).ready(function () {
    var total_cost = 0
    var total_cost_tag = $("#total_cost_number")

    total_cost_tag.text(total_cost)

    $( ".seat_number" ).on('click', function(elem) {
        var seat_number = $(this).text();

        if ( $(this).hasClass('seat_number_chosen')) {
            remove_seat_number_from_input(seat_number);
            total_cost = total_cost - Number($(this).attr('price'))
        }else{
            append_seat_number_to_input(seat_number);
            total_cost = total_cost + Number($(this).attr('price'))
        }

        $(this).toggleClass('seat_number_chosen');
        $(this).toggleClass('seat_number');

        total_cost_tag.text(total_cost)
    });
});

function append_seat_number_to_input(seat_number) {
    var seat_numbers_input = $("#id_seat_numbers");
    var existing_value = seat_numbers_input.val();

    if (seat_already_added(seat_number)) {
        return
    }

    if (existing_value == '') {
        var append_str = seat_number;
    } else {
        var append_str = ',' + seat_number;
    }

    var new_value = existing_value + append_str;
    seat_numbers_input.val(new_value);

};

function seat_already_added(seat_number) {

    var seat_numbers_input = $("#id_seat_numbers");
    var existing_value_array = seat_numbers_input.val().split(",");

    return existing_value_array.includes(seat_number)

};

function remove_seat_number_from_input(seat_number) {
    var seat_numbers_input = $("#id_seat_numbers");
    var existing_value_array = seat_numbers_input.val().split(",");

    const index = existing_value_array.indexOf(seat_number);
    if (index > -1) {
        existing_value_array.splice(index, 1);
    }
    seat_numbers_input.val(existing_value_array);
};