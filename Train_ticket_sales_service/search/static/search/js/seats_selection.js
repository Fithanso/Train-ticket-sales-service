$(document).ready(function () {
    var total_cost = 0
    var total_cost_tag = $("#total_cost_number")

    total_cost_tag.text(total_cost)

    $( ".seat_name" ).on('click', function(elem) {
        var seat_name = $(this).text();

        if ( $(this).hasClass('seat_name_chosen')) {
            remove_seat_name_from_input(seat_name);
            total_cost = total_cost - Number($(this).attr('price'))
        }else{
            append_seat_name_to_input(seat_name);
            total_cost = total_cost + Number($(this).attr('price'))
        }

        $(this).toggleClass('seat_name_chosen');
        $(this).toggleClass('seat_name');

        total_cost_tag.text(total_cost)
    });
});

function append_seat_name_to_input(seat_name) {
    var seat_names_input = $("#id_seat_names");
    var existing_value = seat_names_input.val();

    if (seat_already_added(seat_name)) {
        return
    }

    if (existing_value == '') {
        var append_str = seat_name;
    } else {
        var append_str = ',' + seat_name;
    }

    var new_value = existing_value + append_str;
    seat_names_input.val(new_value);

};

function seat_already_added(seat_name) {

    var seat_names_input = $("#id_seat_names");
    var existing_value_array = seat_names_input.val().split(",");

    return existing_value_array.includes(seat_name)

};

function remove_seat_name_from_input(seat_name) {
    var seat_names_input = $("#id_seat_names");
    var existing_value_array = seat_names_input.val().split(",");

    const index = existing_value_array.indexOf(seat_name);
    if (index > -1) {
        existing_value_array.splice(index, 1);
    }
    seat_names_input.val(existing_value_array);
};