var source = {
    body: $('body'),
    ready: function () {
        if (isMobile())
            source.body.addClass('mobile');
        else
            source.body.addClass('pc');

        set_persian();
        set_copy();
        set_btn();
        set_input();
        set_select();
        set_ranger();
        set_calendar();
        set_line(true);
        set_chart(true);
        source.resize();
        set_weigth();
        set_tab();
        setTimeout(function () {
            set_slide();
            set_masonry();
            source.body.addClass('ready');
        }, 110);
    },
    load: function () {

        var el = $('#banner-image');
        var width = 190 - el.outerWidth();
        if (width < 0)
            width = width / 2;
        el.css('right', width + 'px');


        setTimeout(function () {
            $('[data-src]').each(function () {
                var src = $(this).data('src');
                $(this).attr('src', src).removeAttr('data-src');
            });
        }, 20);

        setTimeout(function () {

            $('#errorModal').modal('show');

            source.body.addClass('load');
            $('.loading-box').css('visibility', 'invisible');
        }, 100);
        set_line(false);
        set_chart(false);
    },
    resize: function () {
        $('.masonry-content').removeClass('set');
        setTimeout(function () {
            var height = document.body.clientHeight;
            var width = document.body.clientWidth;
            $('.body_height').css('height', height + 'px');
            $('.body_min_height').css('min-height', height + 'px');
            $('.body_max_height').css('max-height', height + 'px');
            set_weigth();
            set_masonry();
        }, 100);
    },
    scroll: function () {

    }
};
$(window).resize(source.resize);
$(window).on('load', source.load);
$(window).scroll(source.scroll);
$(document).ready(source.ready);
/////////////////////////////////////////////////////////// event
$(document).on('click', function () {
    $('.form-group.focus').removeClass('focus');
});
$(document).on('focus', '.form-control', function () {
    var el = $(this);
    $('.form-group.focus').removeClass('focus');
    if (el.attr('readonly') || el.attr('disabled')) return;
    setTimeout(function () {
        el.parents('.form-group').addClass('focus');
    }, 100);
});
$(document).on('click', '.form-control', function () {
    var el = $(this);
    $('.form-group.focus').removeClass('focus');
    if (el.attr('readonly') || el.attr('disabled')) return;
    setTimeout(function () {
        el.parents('.form-group').addClass('focus');
    }, 100);
});
$(document).on('change', '.form-control', function () {
    check_input($(this));
});
$(document).on('click', '.notification-item:not(.direct_link)', function () {
    if (!$(this).hasClass('open'))
        $('.notification-item.open').removeClass('open');
    $(this).toggleClass('open').removeClass('new');
    var top = $(this).offset().top - 50;
    $('body,html').animate({scrollTop: top + 'px'}, 800);
});
$(document).on('click', '[data-toggle="tab"]', function () {
    setTimeout(function () {
        set_weigth();
    }, 50);
});
$(document).on('click', '.home-modal-close', function () {
    $(this).parent().fadeOut();
});
$(document).on('click', '.calendar-item', function () {
    var el = $(this);
    var key = el.attr('key');
    var date = el.attr('date');
    var start = el.attr('start');
    var end = el.attr('end');
    var text = el.attr('text');

    $('#calendar_item_day').html(getArabicNumbers(date));
    $('#calendar_item_time').html(getArabicNumbers('از ' + start + ' تا ' + end));
    $('#calendar_item_text').html(text);
    $('#calendar_btn_delete').attr('data-key', key).data('key', key);
    $('#taskShowModal').modal('show');
});
/////////////////////////////////////////////////////////// helper
var set_persian = function () {
    $('.pagination a').addClass('persian_number');
    $('.title').addClass('persian_number');
    $('p').addClass('persian_number');
    $('span').addClass('persian_number');
    $('.persian_number').each(function () {
        $(this).html(getArabicNumbers($(this).html())).removeClass('persian_number');
    });
};
var set_copy = function () {
    $('[data-copy]').each(function () {
        var el = $(this);
        var target = $(el.data('copy'));
        el.removeAttr('data-copy');
        target.html(el.html());
    });
};
var set_btn = function () {
    var taint, d, x, y;
    $(".btn").click(function (e) {
        if ($(this).find(".taint").length == 0) {
            $(this).prepend("<span class='taint'></span>")
        }
        taint = $(this).find(".taint");
        taint.removeClass("drop");
        if (!taint.height() && !taint.width()) {
            d = Math.max($(this).outerWidth(), $(this).outerHeight());
            taint.css({height: d, width: d});
        }
        x = e.pageX - $(this).offset().left - taint.width() / 2;
        y = e.pageY - $(this).offset().top - taint.height() / 2;
        taint.css({top: y + 'px', left: x + 'px'}).addClass("drop");
    });
};
var set_input = function () {
    $('.form-control').each(function () {
        check_input($(this));
    });
};
var check_input = function (input) {
    var val = input.val().trim();
    if (val === '')
        input.parents('.form-group').removeClass('full');
    else
        input.parents('.form-group').addClass('full');

    if (input.attr('readonly'))
        input.parents('.form-group').addClass('readonly');
    else
        input.parents('.form-group').removeClass('readonly');

    if (input.attr('disabled'))
        input.parents('.form-group').addClass('disabled');
    else
        input.parents('.form-group').removeClass('disabled');
};

var set_slide = function () {
    $('.owl-carousel-slide').each(function () {
        var el = $(this);
        el.removeClass('owl-carousel-slide');
        el.owlCarousel({
            rtl: true,
            loop: true,
            margin: 0,
            nav: false,
            dots: true,
            items: 1,
            autoplay: true

        });
    });
    $('.single-activity-slider').each(function () {
        var el = $(this);
        el.removeClass('owl-carousel-slide');
        el.owlCarousel({
            rtl: true,
            loop: true,
            margin: 0,
            nav: false,
            dots: true,
            items: 1,
            autoplay: true
        });
    });

    $('.owl-carousel-tag-slide').each(function () {
        var el = $(this);
        el.removeClass('owl-carousel-tag-slide');
        el.owlCarousel({
            rtl: true,
            loop: true,
            margin: 15,
            nav: false,
            dots: false,
            autoWidth: true,
            items: 1
        });
    });
    $('.owl-carousel-activity').each(function () {
        var el = $(this);
        el.removeClass('owl-carousel-activity');
        el.owlCarousel({
            rtl: true,
            loop: true,
            margin: 13,
            nav: false,
            dots: true,
            responsive: {
                0: {
                    items: 1
                },
                550: {
                    items: 2
                },
                1000: {
                    items: 3
                },
                1200: {
                    items: 4
                }
            }
        });
    });
    set_weigth();
};
var set_weigth = function () {
    var set_size = function (class_name, width_main, height_main) {
        var list = $('.' + class_name);
        for (var i = 0; i < list.length; i++) {
            if (list.eq(i).parents('[role="tabpanel"]').length > 0)
                if (!list.eq(i).parents('[role="tabpanel"]').hasClass('active')) continue;
            var width = list.eq(i).outerWidth();
            if (width > 0) {
                list.css('height', ((width * height_main) / width_main) + 'px');
                break;
            }
        }
    };
    set_size('set_slide', 585, 330);
    set_size('set_home_slide', 370, 257);
    set_size('set_activity', 276, 153);
    set_size('set_shop_banner', 262.5, 147.1);
    set_size('set_shop_banner_big', 541, 147.1);
};
var set_masonry = function () {
    var body_width = document.body.clientWidth;
    $('.masonry-content').each(function () {
        var content = $(this);
        var cols = 0;
        var data = content.data('set').split('|');
        for (var i = 0; i < data.length; i++) {
            var size = data[i].split(':');
            if (parseInt(size[0]) <= body_width) {
                cols = parseInt(size[1]);
                break;
            }
        }

        var col_list = [];
        var main_width = content.outerWidth();
        for (var i = 0; i < cols; i++) col_list.push(0);


        var col = 1;
        var big = 0;
        $('>div', this).each(function () {
            var width = $(this).outerWidth();
            var height = $(this).outerHeight();
            var top = col_list[col - 1];
            var right = (col - 1) * (main_width / cols);
            $(this).css({'top': top + 'px', 'right': right + 'px'});
            $(this).attr('data-col', col);
            col_list[col - 1] += height;
            if (big < col_list[col - 1]) big = col_list[col - 1];
            col++;
            if (col > cols) col = 1;
        });
        content.css({'height': big + 'px'}).addClass('set');
    });
};
var set_select = function () {

    $('select[data-selected]').each(function () {
        var val = $(this).data('selected');
        $('option[value="' + val + '"]', this).attr('selected', 'selected').prop('selected', true);
    });

    $('input[data-check]').each(function () {
        var val = $(this).data('check');
        if ($(this).val() == val) $(this).prop('checked', true);
    });

    $('select.select_wait').each(function () {
        $(this).selectpicker();
        $(this).removeClass('select_wait');
        $(this).addClass('select_set');
    });

    $('select.select_set').each(function () {
        $(this).selectpicker('refresh');
    });
};
var set_ranger = function () {
    var i = 0;
    $('.slider-input').each(function () {
        var el = $(this);
        var from = parseInt(el.attr('from'));
        var to = parseInt(el.attr('to'));
        var single = el.attr('type') === 'single';
        var name = el.attr('name');

        var id = "range_input_" + i;
        var text = '<div class="range-detail" >';
        el.append('<div id="' + id + '" ></div>');
        if (!single) {
            text += '<span class="range-detail-start"></span>';
            text += '<span class="range-detail-end"></span>';
        }
        if (single) {
            text += '<span class="range-detail-end"></span>';
        }
        text += '<input class="hide" name="' + name + '" >';
        text += '</div>';
        el.append(text);


        var input = $('input', el);
        input.val(single ? (to - from) / 2 : from + ',' + to);

        var item = document.getElementById(id);
        noUiSlider.create(item, {
            start: single ? (to - from) / 2 : [from, to],
            connect: single ? [true, false] : true,
            range: {
                'min': from,
                'max': to
            }
        });
        if (!single) {
            var start = el.find('.range-detail-start');
            var end = el.find('.range-detail-end');
            start.html(from);
            start.html(to);
        }
        if (single) {
            var single_end = el.find('.range-detail-end');
        }

        item.noUiSlider.on('update', function (values, handle) {
            if (!single) {
                start.html(getArabicNumbers(parseInt(values[0])));
                end.html(getArabicNumbers(parseInt(values[1])));
            }
            if (single) {
                single_end.html(getArabicNumbers(parseInt(values[0])));
            }
            input.val(single ? values[0] : values[0] + ',' + values[1]);
        });
        i++;
    })
};

var set_tab = function () {
    $('.nav-tabs').each(function () {
        var list = $('li', this);
        list.css('width', (100 / list.length) + '%');
    });


    var width = document.body.clientWidth;

    if (width < 500) width -= 30;
    else width = 470;

    $('.best-list').each(function () {
        var content = $(this);
        var list = $('.nav-tabs li', content);
        $('.nav-scroll', content).css('width', width + 'px');
        $('.nav-tabs', content).css('width', Math.ceil(((width / 3) * list.length)) + 'px');
        list.css('width', (width / 3) + 'px');
    });
};

var set_calendar = function () {
    $('.calendar-content:not(.set)').each(function () {
        var content = $(this);
        content.addClass('set');
        var days = content.hasClass('days');
        var title = content.attr('title');
        content.removeAttr('title');

        var list = [];
        $('item', content).each(function () {
            var el = $(this);
            var item = {};
            item.start = el.attr('time').split('|')[0];
            item.end = el.attr('time').split('|')[1];
            item.key = el.attr('key');
            item.text = el.attr('text');
            item.color = el.attr('color');
            item.date = el.attr('date');
            if (days) item.day = parseInt(el.attr('day'));
            list.push(item);
        });

        content.html('<div class="calendar"></div>');
        content = $('.calendar', content);
        content.html('<div class="head"></div>');
        content.append('<div class="rows" ></div>');

        if (days) {
            $('.rows', content).addClass('days');

            var days = ['', 'ش', '1ش', '2ش', '3ش', '4ش', '5ش', 'ج'];
            for (var i in days)
                $('.head', content).append('<div class="day" >' + getArabicNumbers(days[i]) + '</div>');
        }
        else {
            $('.head', content).html('<div class="single-title" >' + title + '</div>')
        }

        $('.rows', content).append('<div class="items" ></div>');
        for (var i = 0; i < 24; i++) {
            var time = i;
            if (time < 10) time = '0' + time;
            $('.rows', content).append('<div class="calendar-row" ><div class="title" >' + getArabicNumbers(time) + '</div></div>');
        }

        list.forEach(function (item) {
            var start = item.start.split(':');
            start[0] = parseInt(start[0]);
            start[1] = parseInt(start[1]);

            var end = item.end.split(':');
            end[0] = parseInt(end[0]);
            end[1] = parseInt(end[1]);

            var top = start[0] * 30;
            if (start[1] > 0)
                top += start[1] / 2;

            var height = end[0] * 30;
            if (end[1] > 0)
                height += end[1] / 2;
            height -= top;

            var right = 0;
            if (days) {
                right = (item.day - 1) * 12.5;
            }

            $('.items', content).append('<div class="item calendar-item"></div>');
            var el = $('.items .item:last-child', content);
            el.css({
                'top': top + 'px',
                'height': height + 'px',
                'right': right + '%',
                'background-color': '#' + item.color
            });
            el.attr('text', item.text);
            el.attr('start', item.start);
            el.attr('end', item.end);
            el.attr('date', item.date);
            el.attr('key', item.key);
            if (days)
                el.html('<div><i class="fa fa-file-text" ></i></div>');
            else
                el.html('<div><div class="text" style="max-height: ' + height + 'px;" >' + item.text + '</div></div>');
        });
    });
};
var set_line = function (first) {
    if (first) {
        $('.school-line:not(.set)').each(function () {
            $(this).addClass('set');
            $(this).append('<div class="point">' + getArabicNumbers($(this).data('text')) + '</div>');
            $(this).append('<div class="fa fa-' + $(this).data('fa') + '"></div>');
            $(this).append('<div class="on_line" style="width:' + 0 + '%" ></div>');
            $(this).prepend('<div class="out_line" style="width:' + 0 + '%" ></div>');
            $(this).append('<div class="circle"></div>');
            $(this).append('<div class="top_white"></div>');
            $(this).append('<div class="bottom_white"></div>');
            $(this).append('<div class="on_bg"></div>');
        });
        return;
    }
    setTimeout(function () {
        $('.school-line:not(.set_width)').each(function () {
            $(this).addClass('set_width');
            var width = parseInt($(this).data('width'));
            $('.out_line,.on_line', this).css({width: width + '%'});
        });
    }, 200);
};
var set_chart = function (first) {
    if (first) {
        var id = Math.random();
        $('.school-chart:not(.set_width)').each(function () {
            id++;
            var color = '#' + $(this).data('color');
            $(this).addClass('set_width');
            $(this).append('<canvas id="school_chart_' + id + '" width="134" height="134" ></canvas>');
            $(this).append('<div class="point" style="color: ' + color + '">' + getArabicNumbers($(this).data('point')) + '</div>');
            $(this).append('<div class="text" style="color: ' + color + '">' + $(this).data('text') + '</div>');
        });
        return;
    }
    setTimeout(function () {
        $('.school-chart:not(.set_chart)').each(function () {
            var percent = parseFloat($(this).data('percent'));
            var id = $('canvas', this).attr('id');
            var c = document.getElementById(id);
            var ctx = c.getContext("2d");
            var CurrentEndAngle = 0;
            var MainEndAngle = 2 / 100 * percent;
            var color = '#' + $(this).data('color');

            var raf =
                window.requestAnimationFrame ||
                window.mozRequestAnimationFrame ||
                window.webkitRequestAnimationFrame ||
                window.msRequestAnimationFrame;
            window.requestAnimationFrame = raf;

            var draw = function () {
                ctx.clearRect(0, 0, 134, 134);
                CurrentEndAngle += 0.01;
                ctx.beginPath();
                ctx.arc(67, 67, 57, 0 * Math.PI, CurrentEndAngle * Math.PI);
                ctx.lineWidth = 20;
                ctx.strokeStyle = color;
                ctx.stroke();
                if (CurrentEndAngle < MainEndAngle) {
                    requestAnimationFrame(function () {
                        draw()
                    });
                }
            };
            draw();
        });
    }, 200);
};
/////////////////////////////////////////////////////////// function
var number_persian = {0: '۰', 1: '۱', 2: '۲', 3: '۳', 4: '۴', 5: '۵', 6: '۶', 7: '۷', 8: '۸', 9: '۹'};

function getArabicNumbers(str) {
    str = str + "";
    var new_str = "";
    for (var i = 0; i < str.length; i++) {
        new_str += isNumeric(str[i]) ? number_persian[str[i]] : str[i];
    }
    return new_str;
}

function getLittleText(text, length) {
    if (text.length <= length) return text;
    return text.substr(0, length) + '...';
}

function isNumeric(value) {
    value = value + "";
    if (value[0] == '.') return false;
    value = value.replace('.', '');
    if (value.indexOf('.') > -1) return false;
    return /^\d+$/.test(value);
}

function isTouchDevice() {
    return 'ontouchstart' in window        // works on most browsers
        || navigator.maxTouchPoints;       // works on IE10/11 and Surface
};

function isMobile() {
    var isMobile = false;
    if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent)
        || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0, 4))) isMobile = true;
    return isMobile;
}

////////////////////////////////////////////////////////////////// file upload
$(document).on('click', '.multi-file-choose', function (e) {
    e.preventDefault();
    var parent = $(this).parents('.multi-file-content');
    var name = parent.data('name');
    var type = parent.data('type');
    var list = null;
    var item = null;

    switch (type) {
        case "activity-file":
            list = $('.activity-file-list', parent);
            list.append('<div class="activity-file multi-file-item hide" data-type="' + type + '" ></div>');
            item = $('.activity-file:last-child', list);
            item.append('<input type="file" class="multi-file-input hide" name="' + name + '[]">');
            item.append('<div class="name" ></div>');
            item.append('<div class="size" ></div>');
            item.append('<button type="button" class="btn btn-warning multi-file-remove" >حذف</button>');
            item.find('input').first().trigger('click');
            break;
        case "activity-image":
            list = $('.activity-image-list>.row', parent);
            list.append('<div class="col-md-4 col-ps-6 col-xs-12 multi-file-item hide" data-type="' + type + '" ><div class="activity-image" ></div></div>');
            item = $('.multi-file-item:last-child .activity-image', list);
            item.append('<input type="file" class="activity-image multi-file-input hide" name="' + name + '[]">');
            item.append('<a target="_blank" class="image" ></a>');
            item.append('<div class="content" ></div>');
            var content = $('.content', item);
            content.append('<h4 class="title name" ></h4>');
            content.append('<span class="size"></span>');
            content.append('<button type="button" class="btn btn-warning btn-sm multi-file-remove">حذف</button>');
            item.find('input').trigger('click');
            break;
        case "single-image":
            list = $('.activity-image-list>.row', parent);
            list.html('<div class="col-md-4 col-ps-6 col-xs-12 multi-file-item hide" data-type="activity-image" ><div class="activity-image" ></div></div>');
            item = $('.multi-file-item:last-child .activity-image', list);
            item.append('<input type="file" class="activity-image multi-file-input hide" name="' + name + '">');
            item.append('<a target="_blank" class="image" ></a>');
            item.append('<div class="content" ></div>');
            var content = $('.content', item);
            content.append('<h4 class="title name" ></h4>');
            content.append('<span class="size"></span>');
            content.append('<button type="button" class="btn btn-warning btn-sm multi-file-remove">حذف</button>');
            item.find('input').trigger('click');
            break;
    }
});

$(document).on('click', '.multi-file-remove', function (e) {
    e.preventDefault();
    $(this).parents('.multi-file-item').remove();
});

$(document).on('change', '.multi-file-input', function (e) {
    var input = $(this);

    var address = input.val();
    if (address) {
        var content = input.parents('.multi-file-content');
        $('.multi-file-item:not(.hide)', content).each(function () {
            if (address === null) return;
            var add = $(this).data('address');
            if (add == address) address = null;
        });
    }

    var removeEl = function () {
        input.parents('.multi-file-item').remove()
    };

    if (!address) removeEl();
    else {
        var parent = input.parents('.multi-file-item');
        var type = parent.data('type');
        var fileSize = Math.round(input[0].files[0].size / 1024);
        var fileType = input[0].files[0].type;
        var ValidImageTypes = ["image/jpeg", "image/png"];

        switch (type) {
            case "activity-image": {

                if ($.inArray(fileType, ValidImageTypes) < 0) {
                    toastr.error('فقط فایل های jpg و png');
                    removeEl();
                    return;
                }

                var reader = new FileReader();

                reader.onload = function (e) {
                    parent.find('.image').attr('src', e.target.result).css('background-image', 'url(' + e.target.result + ')');
                };

                reader.readAsDataURL(input[0].files[0]);
                break;
            }
            case "activity-file": {

                //maximum count
                var maxCount = parent.parents('.multi-file-content').attr('data-max');
                var minCount = parent.parents('.multi-file-content').attr('data-min');

                var childCount = parent.parents('.multi-file-content').find('.activity-file:not(.hide)').length + 1;
                if (maxCount && minCount) {

                    maxCount = maxCount.split(',');
                    maxCount = maxCount[0];

                    //minimum count
                    minCount = minCount.split(',');
                    minCount = minCount[0];

                    //upladed file count
                    console.log(childCount);


                    if (maxCount !== "-1" && childCount > maxCount) {
                        validator('count');
                    } else {

                        var fileType = input[0].value;

                        //1.    check file type
                        var elementTypes = parent.parents('.multi-file-content').attr('data-formats');

                        //2.    check valid file type
                        elementTypes = elementTypes.split(',');
                        var fileType = fileType.split('.').pop();

                        //3. get valid size
                        var maxSize = parent.parents('.multi-file-content').attr('data-max');
                        var minSize = parent.parents('.multi-file-content').attr('data-min');

                        maxSize = maxSize.split(',');
                        minSize = minSize.split(',');

                        maxSize = maxSize[1];
                        minSize = minSize[1];

                        if (elementTypes.indexOf(fileType) < 0) {
                            validator('type');
                        } else if (maxSize <= fileSize) {

                            validator('size');
                        } else if (minSize >= fileSize) {

                            validator('size');
                        }

                    }

                    function validator(status) {
                        //3.    remove from UI and appear related error
                        switch (status) {
                            case "type":
                                toastr.error('فقط فایل های ' + elementTypes);
                                parent[0].remove();
                                break;

                            case "size":

                                var text = 'حداکثر اندازه ' + maxSize / 1024 + 'MB ';
                                if (minSize > 0) {
                                    text += 'حداقل اندازه ' + minSize / 1024 + 'MB ';
                                }

                                toastr.error(text);
                                parent[0].remove();
                                break;

                            case "count":

                                toastr.error('حداکثر تعداد ' + maxCount);
                                parent[0].remove();
                        }
                    }

                    break;
                }
            }
        }

        var name = input[0].files[0].name;
        var size = Math.floor(input[0].files[0].size / 1024);

        if (size > 1024)
            size = Math.floor(input[0].files[0].size / 1024000) + ' mb';
        else
            size += " kb";
        parent.data('address', address);
        parent.attr('data-address', address);

        parent.find('.name').html(getLittleText(name, 15));
        parent.find('.size').html(getArabicNumbers(size));
        parent.removeClass('hide');
    }
});


$(document).on('submit', 'form', function (e) {
    $('.multi-file-content input[type="file"]', this).each(function () {
        if (!$(this).val()) $(this).parents('.multi-file-item').remove();
    });
    $('.loading-box').css('visibility', 'visible');
});

///////////////////////////////////////////////////////////////// player
var player_el = null;
$(document).on('click', '[data-play]', function (e) {
    e.preventDefault();
    var url = $(this).data('play');
    var flash = $('script#player').attr('src').replace('/jwplayer.js', '/jwplayer.flash.swf');
    $('body').append('<div class="player-modal" ><div><button class="player-modal-close" ></button><div id="player_content_parent" ><div id="player_content" ></div></div></div></div>');

    jwplayer.key = "FgPx4ELq59RhTtTcMl1CO3IDk9Pr5SWnDnqSww==";
    var name = 'player_content';
    player_el = jwplayer(name);
    player_el.setup({
        flashplayer: flash,
        file: url,
        width: '100%',
        aspectratio: "16:9",
        androidhls: 'true',
        primary: 'html5'
    });
    $('.player-modal').addClass('active');
});
$(document).on('click', '.player-modal-close', function (e) {
    e.preventDefault();
    var parent = $('.player-modal');
    parent.removeClass('active');
    player_el.stop();
    setTimeout(function () {
        player_el.remove();
        $('#player_content').detach().remove();
        parent.remove();
    }, 500);
});
$(document).ready(function () {
    toastr.options = {
        closeButton: false,
        debug: false,
        newestOnTop: true,
        progressBar: false,
        positionClass: 'toast-top-left',
        preventDuplicates: true,
        onclick: null
    };
});

// ehsan // tooltip
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

// ehsan // Disabling submit button until all fields have values
// $('button[type="submit"]').prop('disabled', true);

// $form = $('#annual-income'); // cache
// form.find(':input[type="submit"]').prop('disabled', true); // disable submit btn
// form.find(':input').change(function() { // monitor all inputs for changes
//     var disable = false;
//     form.find(':input').not('[type="submit"]').each(function(i, el) { // test all inputs for values
//         if ($.trim(el.value) === '') {
//             disable = true; // disable submit if any of them are still blank
//         }
//     });
//     form.find(':input[type="submit"]').prop('disabled', disable);
// });
//
// function() {
//     $('form').find(':input').keyup(function() {
//         var empty = false;
//         $('form').find(':input').not('[type="submit"]').each {
//             if ($(this).val() == '') {
//                 empty = true;
//             }
//         });
//
//         if (empty) {
//             $('button[type="submit"]').prop('disabled', true);
//         } else {
//             $('button[type="submit"]').prop('disabled', false);
//         }
//     });
// })