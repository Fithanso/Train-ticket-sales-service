$(document).ready(function () {
    $( ".seat_name" ).on('click', function(elem) {
        var seat_name = $(this).text();

        if ( $(this).hasClass('seat_name_chosen')) {
            remove_seat_name_from_input(seat_name);
        }else{
            append_seat_name_to_input(seat_name);
        }

        $(this).toggleClass('seat_name_chosen');
        $(this).toggleClass('seat_name');

        var seat_names_input = $("#id_seat_names");
        console.log(seat_names_input.val());
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