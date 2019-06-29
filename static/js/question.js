function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function load_sub_categories(category_id, targets){

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: "/hamraz/questions/category/" + category_id
    }).done(function(data) {

        var categories = data["categories"]["results"];
        var i;
        var category_item = {};
        var data_len = categories.length;

        targets.forEach(function (target) {
            var category_select = document.getElementById(target);
            $("#" + target).find('option').remove();
            for (i=0; i< data_len; i++) {
                category_item = categories[i];
                var option = document.createElement("option");
                option.text = category_item["title"];
                option.value = category_item["id"];
                category_select.add(option);
            }
            $("#" + target).selectpicker("refresh");
        });
    });
}

function remove_options(targets) {
    targets.forEach(function (target) {
        $("#" + target).find('option').remove();
        $("#" + target).selectpicker("refresh");
    });
}

$(document).ready(function() {

    var category_id = $('#category').val();
    if ($.isNumeric(category_id) ){
        load_sub_categories(category_id, ['sub_category', 'faq_sub_category']);
    }else{
        remove_options(['sub_category', 'faq_sub_category']);
    }

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      var target = $(e.target).attr("aria-controls");
      if (target === "own_q") {
          $("#new_question_btn").removeClass("hidden");
      }else{
          $("#new_question_btn").addClass("hidden");
      }
    });
});

$('#category').on('change', function() {

    var category_id = this.value;
    if ($.isNumeric(category_id) ) {
        load_sub_categories(category_id, ['sub_category']);
    }else{
        remove_options(['sub_category']);
    }
});

$('#faq_category').on('change', function() {

    var category_id = this.value;
    if ($.isNumeric(category_id) ) {
        load_sub_categories(category_id, ['faq_sub_category']);
    }else{
        remove_options(['faq_sub_category']);
    }
});
