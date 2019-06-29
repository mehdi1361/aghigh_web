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

function start_edit_comment(comment_id) {

    var comment_title = $("#comment_title" + comment_id).text();
    $("#comment").val(comment_title);
    var comment_params = $('*[class^=comment_' + comment_id + ']');
    var l = comment_params.length;
    for (var i = 0; i < l; i++) {

        var comment_param = comment_params[i];
        var item_class = comment_param.getAttribute("class");
        var item_class_parts = item_class.split("_");
        var item_value = comment_param.getAttribute("value");

        console.log(item_class_parts);
        console.log(item_value);

        var target_item = document.getElementById("range_input_" + i);
        target_item.noUiSlider.set(item_value);
    }

    $("#edit_comment_id").val(comment_id);

}

function send_comment() {

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var activity_id = $("#activity").val();
    var comment = $("#comment").val();
    var edit_comment_id = $("#edit_comment_id").val();
    var post_data = {};
    post_data["comment"] = comment;
    post_data["edit_comment_id"] = edit_comment_id;
    var p = [];
    var params_items = $(".rohola");
    var l = params_items.length;
    for (var i = 0; i < l; i++) {

        var da = params_items[i];
        p.push({
            "id": parseInt(da.getAttribute("id")),
            "value": parseInt(parseFloat(da.getElementsByClassName('noUi-handle')[0].getAttribute("aria-valuetext")))
        });
    }
    post_data["params"] = p;
    $.ajax({
        url: "/activity/comment/" + activity_id,
        type: "POST",
        data: {
            "data": JSON.stringify(post_data)
        }
    }).done(function (data) {

        // toastr.success('دیدگاه شما ثبت و پس از تایید نمایش داده خواهد شد.');
        toastr.success('دیدگاه شما ثبت شد.');

        location.reload();
        $('#commentModal').modal('toggle');
    });

}

$('#save_comment').on('click', function () {
    send_comment();
});
