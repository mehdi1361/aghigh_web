/**
 * Created by rmaleki on 11/26/17.
 */
var county = "";

function appendPageToUrl(key, value) {
    window.history.replaceState('', '', updateURLParameter(window.location.href, key, value));
    location.reload()
}

function updateURLParameter(url, param, paramVal) {
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";
    if (additionalURL) {
        tempArray = additionalURL.split("&");
        for (var i = 0; i < tempArray.length; i++) {
            if (tempArray[i].split('=')[0] !== param) {
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }
    }
    var rows_txt = "";
    if (paramVal !== "") {
        rows_txt = temp + "" + param + "=" + paramVal;
    }
    return baseURL + "?" + newAdditionalURL + rows_txt;
}

function render_dropdown(data, md, type_field) {
    var html = '<div class="col-sm-' + parseInt(12 / md) + ' col-xs-12">';

    var star = "";
    if (data["required"]) {
        star = "*";
    }


    html += '<div class="form-group style-1 full" style="position: relative;">';
    html += '<label>' + data["label"] + star + '</label>';
    html += '<select onchange="select_sub_form(this)" group-data="' + data['group'] + '" id="' + type_field + data["id"] + '" ';
    html += 'name="' + type_field + data["id"] + '" class="select_wait">';
    if (!data["required"]) {
        html += '<option value="">----</option>';
    }
    data["values"].forEach(function (item) {
        html += '<option data-select="' + item["group_select_id"] + '"  value="' + item["id"] + '">' + item["value"] + '</option>';
    });
    html += '</select></div></div>';

    return html;
}

function render_textbox(data, md, type_field) {
    var html = '<div class="col-sm-' + parseInt(12 / md) + ' col-xs-12">';
    var div_id = type_field + data["id"];

    var star = "";
    if (data["required"]) {
        star = "*";
    }
    html += '<div class="form-group style-1">';
    html += '<label for="">' + data["label"] + star + '</label>';
    html += '<div class="input">';
    if (data["required"]) {
        html += '<textarea name="' + div_id + '" id="' + div_id + '" class="form-control" required oninvalid="setCustomValidity(\'این فیلد اجباری است.\')" oninput="setCustomValidity(\'\')"></textarea>';
    } else {
        html += '<textarea name="' + div_id + '" id="' + div_id + '" class="form-control"></textarea>';
    }
    html += '</div></div></div>';

    return html;
}

function calculator_size(size) {
    size = parseInt(size);
    var new_size = "";
    if (size >= 1024) {
        size = Math.round(size / 1024);
        new_size += size + "mb"
    } else
        new_size += size + "kb";
    return new_size

}

function create_validator(validate_data) {
    var html = "";
    html += "<p class='col-xs-12' style='margin: 10px 0'>";
    if (validate_data['format']) {
        html += "فرمت های مجاز:(";
        for (var i = 0; i < validate_data['format'].length; i++) {
            html += validate_data['format'][i] + ",";
        }
        html += "),"
    }
    if (validate_data['min_file_size'] !== -1) {
        html += "حداقل سایز مجاز: " + calculator_size(validate_data['min_file_size']) + ","
    }
    if (validate_data['max_file_size'] !== -1) {
        html += "حداکثر سایز مجاز: " + calculator_size(validate_data['max_file_size']) + ","
    }
    if (validate_data['min_file_count'] !== -1) {
        html += "حداقل تعداد فایل مجاز: " + validate_data['min_file_count'] + ","
    }
    if (validate_data['max_file_count'] !== -1) {
        html += "حداکثر تعداد فایل مجاز: " + validate_data['max_file_count']
    }
    html += "</p>";
    return html
}

function getMaxCount() {

    setTimeout(function () {

        var getRequired = document.querySelectorAll('.form-group[data-required="true"]').length;

        //if required is in page
        if (getRequired > 0) {
            var btn = document.querySelector('button#submit_activty');
            btn.classList.add('disabled');
            btn.type = "button";

            btn.addEventListener('mouseover', function () {

                var getRequired = document.querySelectorAll('.form-group[data-required="true"]');

                var flag = [];

                var arrayLength = getRequired.length;

                for (var i = 0; i < arrayLength; i++) {

                    var validMin = getRequired[i].getElementsByClassName('multi-file-content')[0];
                    validMin = validMin.getAttribute('data-min');
                    validMin = validMin.split(',');
                    validMin = validMin[0];

                    var ChildCount = getRequired[i].querySelectorAll('.activity-file').length;

                    if (validMin <= ChildCount) {
                        flag[i] = true;
                    } else if (validMin > ChildCount) {
                        flag[i] = false;
                    }

                    function checkIsSame() {
                        var tag = true;
                        flag.forEach(function (cur) {
                            if (!cur) {
                                tag = false;
                            }
                        });
                        return tag;
                    }

                    var state = checkIsSame();

                    if (state) {
                        btn.classList.remove('disabled');
                        btn.type = "submit";
                    } else {
                        btn.classList.add('disabled');
                        btn.type = "button";
                    }

                }

            });
        } else {
            var btn = document.querySelector('button#submit_activty');
            btn.classList.remove('disabled');
            btn.type = "submit";
        }
    }, 1000);
}

function render_file(data, md, type_field) {
    var star = "";
    var required = "false";
    if (data["required"]) {
        star = "*";
        required = "true";
    }
    var div_id = type_field + data["id"];
    var upload_element = "";
    var validator = data['validate_data'];

    if (page_name !== "check") {
        upload_element += '<div class="activity-file-list m-b-30 m-t-30"></div>';
        upload_element += '<p class="text-center m-b-40">';
        upload_element += '<button type="button" class="btn btn-primary multi-file-choose m-b-10">افزودن فایل </button>';
        upload_element += '</p>';
        upload_element += '<script type="text/template" id="">';
        upload_element += '<div class="activity-file" data-number="">';
        upload_element += '<input type="file" name="' + div_id + '_[]">';
        upload_element += '<span class="name">عنوان فایل در اینجا</span>';
        upload_element += '<span class="size persian_number">260 kb</span>';
        upload_element += '<button type="button" class="btn btn-warning">حذف </button>';
        upload_element += '</div>';
        upload_element += '</script>';
    }

    //get data
    var all = data['validate_data'];

    var html = '<div class="form-group style-1 full" data-required="' + required + '"  style="position: relative;">';
    html += create_validator(data['validate_data']);
    html += '<div class="col-sm-12 col-xs-12 multi-file-content" data-formats="' + all['format'].toString() + '" data-max="' + all['max_file_count'] + ',' + all['max_file_size'] + '" data-min="' + all['min_file_count'] + ',' + all['min_file_size'] + '"  id="' + div_id + '" data-name="' + div_id + '_" data-type="activity-file">';
    html += '<label class="m-t-10" for="">' + data["label"] + star + '</label>';
    html += upload_element;
    html += '</div>';
    html += '</div>';
    return html;
}

function render_checkbox(data, md, type_field) {
    var html = '<div class="col-sm-' + parseInt((12 / md) + 1) + ' col-xs-12" style="margin-top: 35px;">';
    var div_id = type_field + data["id"];
    var star = "";
    if (data["required"]) {
        star = "*";
    }

    html += '<div class="form-group style-1 checkbox">';
    html += '<label class="check-ps big fit-width">';
    if (data["required"]) {
        html += '<input type="checkbox" value="off" id="check_' + data["id"] + '" onchange="changeValueCheckbox(this, \'' + div_id + '\')" required >';
    } else {
        html += '<input type="checkbox" value="off" id="check_' + data["id"] + '" onchange="changeValueCheckbox(this, \'' + div_id + '\')" >';
    }
    html += '<span></span>';

    html += '<span>' + data["label"] + star + '</span>';
    html += '</label>';
    html += '<input type="hidden" value="off" name=' + div_id + ' id=' + div_id + '>';
    html += '</div></div>';

    return html;
}

function render_number(data, md, type_field) {
    var html = '<div class="col-sm-' + parseInt(12 / md) + ' col-xs-12">';
    var div_id = type_field + data["id"];

    var star = "";
    if (data["required"]) {
        star = "*";
    }

    html += '<div class="form-group style-1">';
    html += '<label for="">' + data["label"] + star + '</label>';
    html += '<div class="input">';
    if (data["required"]) {
        html += '<input type="number" name=' + div_id + ' id=' + div_id + ' class="form-control" required oninvalid="setCustomValidity(\'این فیلد اجباری است.\')" oninput="setCustomValidity(\'\')">';
    } else {
        html += '<input type="number" name=' + div_id + ' id=' + div_id + ' class="form-control">';
    }
    html += '</div></div></div>';

    return html;
}

function render_recommended(data, md, type_field) {
    var html = '<div class="col-sm-' + parseInt(12 / md) + ' col-xs-12">';
    var div_id = type_field + data["id"];

    var star = "";
    if (data["required"]) {
        star = "*";
    }

    html += '<div class="form-group style-1">';
    html += '<label for="">' + data["label"] + star + '</label>';
    html += '<div class="input">';
    if (data["required"]) {
        html += '<input type="text" name=' + div_id + ' id=' + div_id + ' class="form-control" required oninvalid="setCustomValidity(\'این فیلد اجباری است.\')" oninput="setCustomValidity(\'\')">';
    } else {
        html += '<input type="text" name=' + div_id + ' id=' + div_id + ' class="form-control">';
    }
    html += '</div></div></div>';

    return html;
}

function getColmd(data_len) {
    if (data_len === 4) {
        return 6
    } else if (data_len % 3 === 0) {
        return 3
    }
    else if (data_len % 2 === 0) {
        return 2
    }
    else if (data_len !== 5) {
        return 3
    }
    return data_len
}

function load_selected_box() {
    var selects = document.getElementsByTagName('select');
    for (var z = 0; z < selects.length; z++) {
        $(selects[z]).selectpicker();
    }
}

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

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function load_province_cities(province_id) {

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: "/cities/" + province_id
    }).done(function (data) {

        var cities = data["cities"];
        var i;
        var city_item = {};
        var data_len = cities.length;
        var city_select = document.getElementById("county");
        $("#county").find('option').remove();
        var option = document.createElement("option");
        option.text = "همه شهرها";
        option.value = "";
        city_select.add(option);

        for (i = 0; i < data_len; i++) {
            city_item = cities[i];
            option = document.createElement("option");
            option.text = city_item["title"];
            option.value = city_item["id"];
            if (county.toString() === city_item["id"].toString()) {
                option.selected = true;
            }
            city_select.add(option);
        }
        $("#county").selectpicker("refresh");
    });

}

$('#province').on('change', function () {
    var province_id = this.value;
    if (province_id) {
        load_province_cities(province_id);
    } else {
        $("#county").find('option').remove();
        $("#county").selectpicker("refresh");

    }
});

//error message on dont import required files
var submitButton = document.querySelector('button#submit_activty');
if (submitButton) {
    submitButton.addEventListener('click', function () {

        var type = submitButton.getAttribute('type');
        if (type == 'button') {
            toastr.error('فایل های ضروری را آپلود کنید');
        }

    });
}

function changeValueCheckbox(e, id) {
    var checked = $(e).prop('checked');
    if (checked) {
        $("#" + id).val('on')
    } else {
        $("#" + id).val('off')
    }
}

function previousPage() {
    appendPageToUrl('page', parseInt($(".page-item.active").attr('data-page')) - 1)
}

function nexPage(page) {
    if (typeof page !== 'undefined') {
        appendPageToUrl('page', page)
    } else {
        appendPageToUrl('page', parseInt($(".page-item.active").attr('data-page')) + 1)

    }
}