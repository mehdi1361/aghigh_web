var new_receivers = [];
var receivers = [];
/*function status_display_date() {
    var check_bux_input = $("input[name=has_date]");
    var select_date = $("#select_date");
    if (check_bux_input.is(':checked')) {
        select_date.show();
    } else {
        $("input[name=date]").val("");
        select_date.hide();
    }
}*/
function add_announcement_receiver(top_level, gender) {
    $("#header_table").show();
    var str = "";
    var user_type = $("select[name=user_type]").find(":selected");
    var province = $("select[name=province]").find(":selected");
    var county = $("select[name=county]").find(":selected");
    var camp = $("select[name=camp]").find(":selected");
    var gender_type = $("select[name=gender_type]").find(":selected");
    var dict_key = Math.floor(Math.random() * 10546);
    var receiver = {
        "user_type": user_type.val(),
        "province": province.val() !== undefined ? province.val() : "",
        "county": county.val() !== undefined ? county.val() : "",
        "camp": camp.val(),
        "gender": gender_type.val() !== undefined ? gender_type.val() : ""
    };

    if (receiver_not_duplicate(receiver)) {
        receiver.dict_key = dict_key;
        receivers.push(receiver);
        new_receivers.push(receiver);
        $("input[name=receivers]").val(JSON.stringify(new_receivers));

        str += '<tr><td>' + user_type.text() + '</td>';
        if (top_level === "country") {
            str += '<td>' + province.text() + '</td>';
        }
        if (top_level === "province" || top_level === "country") {
            str += '<td>' + county.text() + '</td>';
        }
        if (gender === "True") {
            str += '<td>' + gender_type.text() + '</td>';
        }
        str += '<td>' + camp.text() + '</td>' +
            '<td onclick="remove_announcement_receiver(this,' + dict_key + ')" >' +
            '<button type="button" class="btn btn-danger">حذف </button>' +
            '</td>' +
            '</tr>';
        $("#announcement_receiver_list").append(str);
    }
    else {
        toastr.error("این دریافت کننده قبلا انتخاب شده است.")
        // toastr.error(gettext("this receiver previous selected"))
    }

}
function receiver_not_duplicate(receiver) {
    var temp_receivers = JSON.parse(JSON.stringify(receivers));
    for (var ii=0;ii<temp_receivers.length;ii++){
        var receiver_item = temp_receivers[ii];
        delete receiver_item.dict_key;
        if (JSON.stringify(receiver_item) === JSON.stringify(receiver)){
            return false;
        }
    }
    return true
}
function remove_announcement_receiver(remove_button, dict_key) {
    for (var i = 0; i < new_receivers.length; i++) {
        var receiver = new_receivers[i];
        if (receiver['dict_key'] === dict_key) {
            new_receivers.splice(i, 1)
        }
    }
    for (var j = 0; j < receivers.length; j++) {
        var receiver2 = receivers[j];
        if (receiver2['dict_key'] === dict_key) {
            receivers.splice(j, 1)
        }
    }
    $("input[name=receivers]").val(JSON.stringify(new_receivers));
    remove_button.parentElement.remove();
    if ($("#announcement_receiver_list").find("> tr")['length'] === 0) {
        $("#header_table").hide();
    }
}