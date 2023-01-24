$(document).ready(function () {
(function time_getter() {
  var time_container = $("#time_container");
  var tz = $("#id_customers_timezone").val()
  var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
  var update_timeout_ms = 60000

  $.ajax({
    type: 'POST',
    url: '/api/get_time_by_address/',
    data:  {
        'csrfmiddlewaretoken': csrf_token,
        'address': tz
    },
    success: function(time) {
      time_container.text(time);
    },
    complete: function() {
      setTimeout(time_getter, update_timeout_ms);
    }
  });
})();
});