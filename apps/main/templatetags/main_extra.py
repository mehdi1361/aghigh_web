import json

from django.template import Library
from django.conf import settings

from apps.main.views import BaseViewClass
from utils.hashids import Hashids
from apps.access.acl import acl_view_segment
import requests

register = Library()


@register.filter
def server_url(image):
    return str(settings.SERVER_URL) + ":" + str(settings.SERVER_PORT) + image


@register.filter
def server_public_url(image, size=None):
    if size:
        image_split = image.split(".")
        _image = size + "." + image_split.pop(-1)
        image = ""
        for i in image_split:
            image += i + "."
        return str(settings.MAIN_SERVER_IMAGE_FULL_URL) + image + _image
    return str(settings.MAIN_SERVER_IMAGE_FULL_URL) + image


@register.filter
def check_extension(file):
    if file:
        extension = file.split(".")[-1].upper()
        list_extension = [
            # "3GP",
            # "AVI",
            # "FLV",
            "MOV",
            "MP4",
            # "MPG",
            # "VOB",
            # "WMV",
            # "AIF",
            # "IFF",
            # "M3U",
            # "M4A",
            # "MID",
            "MP3",
            # "MPA",
            "WAV",
            # "WMA"
            "OGG",
            "WEBM",
            "FLAC",
        ]
        if extension in list_extension:
            return True
        return False
    else:
        return False


@register.filter
def to_hash_id(value):
    try:
        hash_ids = Hashids(min_length=8, salt=settings.SECRET_KEY)
        hash_id = hash_ids.encode(int(value))
        return hash_id
    except:
        return 1


@register.filter
def get_color_review_state(review_state):
    state = {
        "green": "#1fb300",
        "yellow": "#ffbf00",
        "red": "#fe1100",
        "dark": "#ffbcbc"
    }
    return state.get(review_state)


@register.filter
def has_perm(request, url):
    user_type = request.user.userbox.user_type

    acl = []
    if user_type == "teacher" or user_type == "advisor":
        try:
            user_level = [request.user.userbox.role_select]
        except:
            user_level = request.user.userbox.user_level.split(',')

        for item in user_level:
            acl += acl_view_segment.get(item, [])

    elif user_type == "student":
        acl = acl_view_segment['student']

    if url not in acl:
        return False

    return True


@register.filter
def user_permission(request):
    user_type = request.user.userbox.user_type

    acl = []
    if user_type == "teacher" or user_type == "advisor":
        try:
            user_level = [request.user.userbox.role_select]
        except:
            user_level = request.user.userbox.user_level.split(',')

        for item in user_level:
            acl += acl_view_segment.get(item, [])

    elif user_type == "student":
        acl = acl_view_segment['student']

    return acl


@register.filter
def get_levels(request):
    user_level = request.user.userbox.user_level
    levels = []
    dict_level = {
        "coach": "مربی",
        "camp": "مسئول و معاون اتحادیه استان",
        "county": "مسئول شهرستان",
        "province": "مسئول استان",
        "province_f": "معاون استان خواهران",
        "province_m": "معاون استان برادران",
        "expert": "مشاور",
        "top_expert": "مشاور ارشد",
        "advisor": "کارشناس",
        "country": "مسئول کل"
    }

    for level in user_level.split(','):
        if level != "" and level in dict_level.keys():
            levels.append({
                "id": level,
                "presentation": dict_level[level]
            })

    return levels


@register.filter
def show_levels(request):
    user_level = request.user.userbox.user_level
    levels = ""
    dict_level = {
        "coach": "مربی",
        "camp": "مسئول و معاون اتحادیه استان",
        "county": "مسئول شهرستان",
        "province": "مسئول استان",
        "province_f": "معاون استان خواهران",
        "province_m": "معاون استان برادران",
        "country": "مسئول کل"
    }
    user_level = user_level.split(',')
    for level in user_level:
        if level != "" and level in dict_level.keys():
            levels += dict_level[level] + ","

    return levels


@register.filter
def get_levels_advisor(request):
    user_level = request.user.userbox.user_level
    levels = []
    dict_level = {
        # "advisor": "کارشناس",
        "expert": "مشاور",
        "top_expert": "کارشناس ارشد",
    }

    for level in user_level.split(','):
        if level != "" and level in dict_level.keys():
            levels.append({
                "id": level,
                "presentation": dict_level[level]
            })

    return levels


@register.filter
def has_perm_both_gender(request):
    user_level = request.user.userbox.user_level
    levels = user_level.split(',')

    if "province" in levels or "county" in levels or "country" in levels:
        return True
    return False


@register.filter
def get_zfill(number):
    return str(number).zfill(2)


@register.filter
def get_day_name(number):
    return dict({
        0: "شنبه",
        1: "یکشنبه",
        2: "دوشنبه",
        3: "سه شنبه",
        4: "چهارشنبه",
        5: "پنج شنبه",
        6: "جمعه",
    })[number]


@register.filter
def get_persian_title_number(number):
    return dict({
        1: "اول",
        2: "دوم",
        3: "سوم",
    })[number]


@register.filter
def get_class(number):
    try:
        class_color = dict({
            1: "gold",
            2: "silver",
            3: "bronze",
        })[number]
    except:
        class_color = ""

    return class_color


@register.filter
def get_app_link_student(va):
    try:
        get_res_app = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/apk_release/student",
        ).json()
        app = str(settings.SERVER_PUBLIC_FULL_URL) + get_res_app["file"]

        return app
    except:
        return ""

# @register.simple_tag()
# def get_app_link_student():
#     try:
#         get_res_app = requests.get(
#             url=settings.SERVER_FULL_URL + "/api/v1/apk_release/student",
#         ).json()
#         app = str(settings.SERVER_PUBLIC_FULL_URL) + get_res_app["file"]
#         download_name = get_res_app['type'] + str(get_res_app['version']) + ".apk"
#         return {'link': app, 'download_name': download_name}
#     except:
#         return {'link': "", 'download_name': ""}


@register.filter
def get_app_link_teacher(va):
    try:
        get_res_app = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/apk_release/teacher",
        ).json()
        app = str(settings.SERVER_PUBLIC_FULL_URL) + get_res_app["file"]

        return app
    except:
        return ""


@register.filter
def get_app_link_hamraz(va):
    try:
        get_res_app = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/apk_release/hamraz",
        ).json()
        app = str(settings.SERVER_PUBLIC_FULL_URL) + get_res_app["file"]

        return app
    except:
        return ""


@register.filter
def get_count_product_in_basket(request):
    get_res = requests.get(
        url=settings.SERVER_FULL_URL + "/api/v1/basket/get_count_product_in_basket/",
        headers=BaseViewClass.get_http_header(request)
    )
    try:
        count = get_res.json()["count"]
    except:
        count = 0
    return count


@register.filter
def get_count_sub_menu(request):
    """
        workspace_index
        index_report
        product_index_manager
    """
    count = 0
    if has_perm(request, 'workspace_index'):
        count += 1
    if has_perm(request, 'index_report'):
        count += 1
    if has_perm(request, 'product_index_manager'):
        count += 1
    if has_perm(request, 'posted_announcement'):
        count += 1
    if has_perm(request, 'all_report_abuses'):
        count += 1

    return count


@register.simple_tag()
def get_site_address():
    return settings.SERVER_FULL_URL
