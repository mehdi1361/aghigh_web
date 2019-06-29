import requests
from enum import unique, Enum
from utils.date_converter import to_julian
from django.conf import settings
from apps.main.views import BaseViewClass
from django.utils.translation import gettext_lazy as _


def get_top_level(request):
    user_level = request.user.userbox.user_level
    user_levels = user_level.split(',')
    top_level = request.GET.get("role")
    if not top_level or top_level not in user_levels:
        if "country" in user_levels:
            top_level = 'country'

        elif "province" in user_levels or 'province_m' in user_levels or 'province_f' in user_levels:
            top_level = 'province'

        elif "county" in user_levels:
            top_level = 'county'

        elif "camp" in user_levels:
            top_level = 'camp'

        elif "coach" in user_levels:
            top_level = 'coach'
    return top_level


def get_sub_levels(request):
    user_level = request.user.userbox.user_level
    user_levels = user_level.split(',')
    sub_levels = [
        {"name": "student", "display_name": _("students")},
        {"name": "coach", "display_name": _("coaches")}
    ]

    if "country" in user_levels:
        sub_levels.append({"name": "camp", "display_name": _("camps")})
        sub_levels.append({"name": "county", "display_name": _("counties")})
        sub_levels.append({"name": "province", "display_name": _("provinces")})
        sub_levels.append({"name": "country", "display_name": _("countries")})

    elif "province" in user_levels or 'province_m' in user_levels or 'province_f' in user_levels:
        sub_levels.append({"name": "camp", "display_name": _("camps")})
        sub_levels.append({"name": "county", "display_name": _("counties")})

    elif "county" in user_levels:
        sub_levels.append({"name": "camp", "display_name": _("camps")})

    return sub_levels


def convert_date_milady(date, has_time=True):
    try:
        if has_time:
            dates = date.split(' ')
            date = to_julian(dates[0])
            date = date + "T" + dates[1]
        else:
            date = to_julian(date)

        return date
    except:
        return ""


def set_data_has_access_to_area(context, request, top_level):
    if top_level == "country":
        try:
            get_res = requests.get(
                url=settings.SERVER_FULL_URL + "/api/v1/provinces/",
                headers=BaseViewClass.get_http_header(request),
            )
            context['provinces'] = get_res.json()["results"]

        except:
            context['provinces'] = []

    elif top_level == "province":
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/counties/",
            headers=BaseViewClass.get_http_header(request),
        )

        try:
            context['counties'] = get_res.json()
        except:
            context['counties'] = []

    elif top_level == "county":
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/camps/",
            headers=BaseViewClass.get_http_header(request),
        )

        try:
            context['camps'] = get_res.json()
        except:
            context['camps'] = []


@unique
class PartProject(Enum):
    # کلاس بخش های مختلف پروژه برای پاس دادن به تابع زیر و برای خوانایی بیشتر کدهای برنامه

    activity = 1000,
    activity_show = 1001,
    activity_create = 1002,
    activity_star = 1003,
    activity_comment = 1004,
    activity_search = 1005,
    activity_rate_users = 1006,
    activity_check = 1007,
    activity_update = 1008,

    question = 2000,
    question_create = 2001,
    question_answer = 2002,
    question_search = 2003,
    question_score = 2004,

    shop = 3000,
    shop_buy = 3001,
    shop_search = 3002,
    shop_create = 3003,

    schedule = 4000,
    schedule_add = 4001,
    schedule_del = 4002,
    schedule_announcements = 4003,
    schedule_search = 4004,

    league = 5000,
    league_search = 5001,
    # league_search = 5001,

    report = 7000,

    emtiaz = 8000,
    emtiaz_search = 8001,

    announcement = 9000,
    announcement_read = 9001,

    notification = 10000,


class DisableManager(object):
    """    کلاس مربوط به اینکه بخش های مختلف برنامه غیرفعال است یا نه
    یا اینکه در چه تاریخی غیرفعال است

    """

    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __str__(self):
        return self.name_part

    # id_part = 0
    # parent_id = 0
    # name_part = ""
    # status = False
    # status_current = True
    # admin_access = True
    # message_disable = ""
    # start_date_disable = datetime.datetime.now()
    # end_date_disable = datetime.datetime.now()
    # hidden = False
    # color = ""
    # alpha = 0.0
    #
    # def __int__(self, id_part, name_part, parent_id, status_current, status, admin_access, message_disable, start_date, end_date, hidden, color, alpha):
    #     self.id_part = id_part
    #     self.name_part = name_part
    #     if self.parent_id:
    #         self.parent_id = parent_id
    #     if self.status:
    #         self.status = status
    #     if self.status_current:
    #         self.status_current = status_current
    #     if self.admin_access:
    #         self.admin_access = admin_access
    #     if self.message_disable:
    #         self.message_disable = message_disable
    #     if self.start_date_disable:
    #         self.start_date_disable = start_date
    #     if self.end_date_disable:
    #         self.end_date_disable = end_date
    #     if self.hidden:
    #         self.hidden = hidden
    #     if self.color:
    #         self.color = color
    #     if self.alpha:
    #         self.alpha = alpha
