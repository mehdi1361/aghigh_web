var additional_fields = [];
var page_name = "";
var deleted_images = [];
var deleted_files = [];
var deleted_additional_files = [];
var select_type_field = "";
var select_key = "";
var additional_fields_id_unick = [];

var data_check_activity = {
    'additional_field': [],
    'general': [],
    'image': [],
    'file': [],
    'additional_files': []
};

$('#category').on('change', function (ca) {

    var category_id = this.value;
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: "/activity/additional_fields/" + category_id
    }).done(function (data) {

        var additional_fields_container = $("#additional_fields_container");
        additional_fields_container.html('');
        var groups = data["groups"];
        var item = {};
        for (var k = 0; k < groups.length; k++) {
            additional_fields_container.append(
                '<div class="section-title style-1" style="display: grid">' +
                '<h3 class="title">' +
                '<span>' + groups[k]["label"] + ':</span>' +
                '</h3>' +
                '<div id="group_' + groups[k]["id"] + '"></div>' +
                '</div>' +
                '<div id="sub_form_group_' + groups[k]["id"] + '"></div>' +
                '</div>'
            )
        }
        for (var j = 0; j < groups.length; j++) {
            var data_len = groups[j]["additional_fields"].length;
            var col_md = getColmd(data_len);
            for (var i = 0; i < data_len; i++) {

                item = groups[j]["additional_fields"][i];
                var group_div = "#group_" + groups[j]["id"];
                switch (item["field_type"]) {

                    case "text_box":
                        $(group_div).append(render_textbox(item, col_md, "additional_fields"));
                        break;
                    case "number":
                        $(group_div).append(render_number(item, col_md, "additional_fields"));
                        break;

                    case "check_box":
                        $(group_div).css("margin-bottom", "52px");
                        $(group_div).css("margin-top", "-45px");
                        $(group_div).append(render_checkbox(item, col_md, "additional_fields"));
                        break;

                    case "recommended":
                        $(group_div).append(render_recommended(item, col_md, "additional_fields"));
                        break;

                    case "drop_down":
                        $(group_div).append(render_dropdown(item, col_md, "additional_fields"));
                        if (page_name === "submit") {
                            $("#additional_fields" + item['id']).change();
                        }
                        break;

                    case "file_upload":
                        $(group_div).append(render_file(item, col_md, "additional_fields_files_"));
                        break;
                }
            }
        }
        add_additional_field_value();
        load_selected_box();
        if (page_name === 'update') {
            enable_btn_submit();

        }
        if (page_name === 'submit') {
            getMaxCount();
        }
    });
});

function select_sub_form(e) {

// تابعی برای لود اطلاعات ساب فرم انتخاب شده
    var sub_form_id = $('option:selected', e).attr("data-select");
    if (sub_form_id === "null" || sub_form_id === undefined || sub_form_id === "-1") {
    } else {
        $.ajax({
            url: "/activity/get_sub_form/" + sub_form_id
        }).done(function (data) {
            show_data_for_sub_form(data, $(e).attr("group-data"));
        })
    }

}

function show_data_for_sub_form(data, sub_form_div_id) {

    var sub_form_container = $("#sub_form_group_" + sub_form_div_id).html('');

    var groups = data["groups"];
    var item = {};
    for (var k = 0; k < groups.length; k++) {
        sub_form_container.append(
            '<div class="section-title style-1" style="display: grid">' +
            '<h3 class="title">' +
            '<span>' + groups[k]["label"] + ':</span>' +
            '</h3>' +
            '<div id="group_' + groups[k]["id"] + '">' +
            '</div>' +
            '<div id="sub_form_group_' + groups[k]["id"] + '"></div>' +
            '</div>' +
            '</div>'
        )
    }
    for (var j = 0; j < groups.length; j++) {
        var data_len = groups[j]["additional_fields"].length;
        var col_md = getColmd(data_len);
        for (var i = 0; i < data_len; i++) {

            item = groups[j]["additional_fields"][i];
            var group_div = "#group_" + groups[j]["id"];
            switch (item["field_type"]) {

                case "text_box":
                    $(group_div).append(render_textbox(item, col_md, "additional_fields"));
                    break;
                case "number":
                    $(group_div).append(render_number(item, col_md, "additional_fields"));
                    break;

                case "check_box":
                    $(group_div).css("margin-bottom", "52px");
                    $(group_div).css("margin-top", "-45px");
                    $(group_div).append(render_checkbox(item, col_md, "additional_fields"));
                    break;

                case "recommended":
                    $(group_div).append(render_recommended(item, col_md, "additional_fields"));
                    break;

                case "drop_down":
                    $(group_div).append(render_dropdown(item, col_md, "additional_fields"));
                    if (page_name === "submit") {
                        $("#additional_fields" + item['id']).change();
                    }
                    break;

                case "file_upload":
                    $(group_div).append(render_file(item, col_md, "additional_fields_files_"));
                    break;
            }
        }
    }
    add_additional_field_value();
    load_selected_box();
    if (page_name === 'update') {
        enable_btn_submit();
    }
    if (page_name === 'submit') {
        getMaxCount();
    }
}

function add_files_for_additional_fields(additional_fields) {
    var db_id = additional_fields["additional_field"].toString();
    var id_element = "#additional_fields_files_" + db_id;
    var row_id = additional_fields['id'];
    var comment_element = additional_fields["comment"];
    var status_element = additional_fields["status"];
    var show_confirm = "";
    var show_comment = "";
    var back_color = "#ffe5e5";

    if (page_name === "update" && !status_element) {
        show_comment += '<button type="button" onclick="delete_additional_file(\'' + row_id + '\');multi_file_choose()"' +
            'class="btn btn-warning">حذف' +
            '</button>' +
            '<div class="form-group style-1" style="padding-top: 0 !important;">' +
            '<div class="input" style="border-bottom: inherit !important;">' +
            '<div class="input-button">' +
            '<button type="button" class="red"' +
            'onclick="showMessage(\'' + comment_element + '\')">' +
            '<i class="fa fa-file-text"></i>' +
            '</button>' +
            '</div>' +
            '</div>' +
            '</div>'
    } else if (page_name === "check" && !status_element) {
        show_confirm += '<div class="form-group" style="margin-top: -10px">' +
            '<div class="input-button pull-left" style="position: inherit !important;">' +
            '<button type="button" class="green" onclick="acceptField(\'additional_files\',' + row_id + ')"><i class="fa fa-check-circle"></i> </button>' +
            '<button type="button" class="red" onclick="openModal(\'additional_files\',' + row_id + ')">' +
            '<i class="fa fa-times-circle"></i>' +
            '</button>' +
            '</div>' +
            '</div>'
    }

    if (status_element) {
        back_color = "#e5fff0"
    }
    var file_html = '<div class="activity-file-list m-b-30" style="margin-top: 40px;">' +
        '<div id="additional_files-' + row_id + '" class="activity-file" style="background: ' + back_color + ';">' +

        '<span class="name">' + additional_fields['value']['title'] + '</span>' +
        '<span class="size">' + additional_fields['value']['size'] + '</span>' +
        '<a class="btn btn-primary" target="_blank" href="' + site_address + additional_fields['value']['path'] + '" download>دانلود </a>' + show_comment +
        '</div>' + show_confirm +
        '</div>';
    $(id_element).append(file_html);
}

function add_additional_field_value() {
    for (var item in additional_fields) {
        var db_id = additional_fields[item]["additional_field"].toString();
        var id_element = "#additional_fields" + db_id;
        var value_element = additional_fields[item]["value"];
        var comment_element = additional_fields[item]["comment"];
        var status_element = additional_fields[item]["status"];

        if (additional_fields[item]['field_type'] === "file_upload") {
            if ($("#additional_files-" + additional_fields[item]['id']).length === 0) {
                add_files_for_additional_fields(additional_fields[item])
            }
        }
        if (additional_fields_id_unick.includes(db_id)) {
            continue
        } else {
            if ($(id_element).length !== 0) {
                additional_fields_id_unick.push(db_id);
            }
        }
        $(id_element).val(value_element);

        if (page_name !== "submit") {
            $(id_element).change();
        }
        if ($(id_element) === '') {
            $(id_element).parents('.form-group').removeClass('full');
        } else {
            $(id_element).parents('.form-group').addClass('full');
        }

        if ($("#check_" + additional_fields[item]["additional_field"]).is(':checkbox')) {
            if (value_element === "on") {
                $("#check_" + (additional_fields[item]["additional_field"]).toString()).prop('checked', true);
                $(id_element).val('on')
            }
        }
        if (status_element) {
            $(id_element).prop("disabled", true);
            $(id_element).parents('.form-group.style-1').wrapInner('<div id="additional_field_' + db_id + '_1" class="input-success"></div>');
        } else {
            $(id_element).parents('.form-group.style-1').wrapInner('<div  id="additional_field_' + db_id + '_1" class="input-danger"></div>');

            if (page_name === "update") {
                $(id_element).before(
                    '<div class="input-button">' +
                    '<button type="button" class="red" onclick="showMessage(\'' + comment_element + '\')">' +
                    '<i class="fa fa-file-text"></i>' +
                    '</button>' +
                    '</div>'
                );
            } else {
                $(id_element).after(
                    '<div class="input-button" id="additional_field_' + db_id + '">' +
                    '<button type="button" class="green"' +
                    'onclick="acceptField(\'additional_field\', ' + db_id + ')">' +
                    '<i class="fa fa-check-circle"></i>' +
                    '</button>' +
                    '<button type="button" class="red"' +
                    'onclick="openModal(\'additional_field\', ' + db_id + ')">' +
                    '<i class="fa fa-times-circle"></i>' +
                    '</button>' +
                    '</div>'
                );
            }
        }
        if (page_name === "check") {
            var form = document.getElementById("data-activity");
            var elements = form.elements;
            for (var i = 0, len = elements.length; i < len; ++i) {
                if (elements[i].type === "text" || elements[i].type === "select-one" || elements[i].type === "number" || elements[i].type === "textarea" || elements[i].type === "checkbox") {
                    elements[i].disabled = true;
                }
            }
        }
    }
}

function delete_image(id) {
    deleted_images.push(id);
    $("#image-" + id).remove();
    $("#deleted_images").val(deleted_images)

}

function delete_file(id) {
    deleted_files.push(id);
    $("#file-" + id).remove();
    $("#deleted_files").val(deleted_files)
}

function delete_additional_file(id) {
    deleted_additional_files.push(id);
    $("#additional_files-" + id).remove();
    $("#deleted_additional_files").val(deleted_additional_files)
}


function openModal(type_field, key) {
    select_type_field = type_field;
    select_key = key;
    $('#noteModal').modal('show');
    set_old_comment_if_exist(type_field, key);
}

function set_old_comment_if_exist(type_field, key) {
    var i = 0;
    var len = data_check_activity[type_field].length;
    for (i; i < len; i++) {
        if (data_check_activity[type_field][i]["id"] === key) {
            $("#comment_deny").val(data_check_activity[type_field][i]["comment"]);
            return
        }
    }
}

function cleanTextArea() {
    $("#comment_deny").val('')
}

function denyField() {
    check_and_remove_key_if_exist(select_type_field, select_key);

    var comment_div = "#comment_deny";
    data_check_activity[select_type_field].push({
        'id': select_key,
        'status': false,
        'comment': $(comment_div).val()
    });

    if (select_type_field === 'image') {
        $("#" + select_type_field + "-" + select_key + " .activity-image").css('background', '#ffbcbc')

    } else if (select_type_field === 'file') {
        $("#" + select_type_field + "-" + select_key).css('background', '#ffe5e5')

    } else if (select_type_field === 'additional_files') {
        $("#" + select_type_field + "-" + select_key).css('background', '#ffe5e5')

    } else {
        $("#" + select_type_field + "_" + select_key + "_1").removeClass('input-success').addClass('input-danger');
        if (select_key === "category") {
            $("#general_category_1").css('background', '#ffe5e5')
        }

    }
    $(comment_div).val('')
}

function acceptField(type_field, key) {
    check_and_remove_key_if_exist(type_field, key);

    data_check_activity[type_field].push({
        'id': key,
        'status': true,
        'comment': ""
    });

    if (type_field === 'image') {
        $("#" + type_field + "-" + key + " .activity-image").css('background', '#e5fff0')

    } else if (type_field === 'file') {
        $("#" + type_field + "-" + key).css('background', '#e5fff0')

    } else if (type_field === 'additional_files') {
        $("#" + type_field + "-" + key).css('background', '#e5fff0')

    } else {
        $("#" + type_field + "_" + key + "_1").removeClass('input-danger').addClass('input-success');
        if (key === "category") {
            $("#general_category_1").css('background', '#e5fff0')
        }

    }
}

function check_and_remove_key_if_exist(type_field, key) {
    var i = 0;
    var len = data_check_activity[type_field].length;
    for (i; i < len; i++) {
        if (data_check_activity[type_field][i]["id"] === key) {
            var item_delete = data_check_activity[type_field].splice(i, 1)[0];
            return
        }
    }
}

function showMessage(comment) {
    if (comment !== "") {
        $('#comment_note').html(comment);

    } else {
        $('#comment_note').html('مربی توضیحی در مورد دلیل رد کردن فیلد وارد نکرده است.');

    }
    $('#noteModal').modal('show');
}

