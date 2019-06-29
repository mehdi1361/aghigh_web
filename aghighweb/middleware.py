import requests
import datetime
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import resolve, reverse
from django.contrib import auth
from apps.access.acl import acl_view_segment
from django.shortcuts import render, redirect
from apps.access.disable import disable_acl_map

from apps.main.utils import DisableManager
from apps.main.views import page_permission_denied_view, page_disable_view


class ACLMiddleware(MiddlewareMixin):
    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            return

        current_url = resolve(request.path_info).url_name

        if current_url in getattr(settings, 'ACL_EXEMPT_VIEWS', set()):
            return

        try:
            user_type = request.user.userbox.user_type
        except:
            try:
                auth.logout(request)
                return render(request, "apps/access/login.html")
            except:
                return render(request, "apps/access/login.html")

        acl = []
        if user_type == "teacher" or user_type == "advisor":
            role_select = request.user.userbox.role_select
            # user_level = request.user.userbox.user_level
            # user_level = user_level.split(',')
            # for item in user_level:
            #     acl += acl_view_segment.get(item, [])
            acl += acl_view_segment.get(role_select, [])


        elif user_type == "student":
            acl = acl_view_segment['student']

        if current_url not in acl:
            if user_type == "student" or user_type == "teacher":
                return redirect(reverse("main_index"))

            elif user_type == "advisor":
                return redirect(reverse("question_manager_index"))

            else:
                return page_permission_denied_view(request)


class DisablePartManager(MiddlewareMixin):
    app_list_disable = []
    app_list_disable_str = []
    app_list_disable_str_for_admin = []

    date_time_load_list = None

    @staticmethod
    def load_app_list():
        DisablePartManager.app_list_disable = []
        DisablePartManager.app_list_disable_str = []

        DisablePartManager.app_list_disable_str_for_admin = []

        DisablePartManager.app_dict_disable = {}

        url = settings.SERVER_FULL_URL + '/static/DisableManager.json'

        data = requests.get(url).json()
        for item in data:
            item_obj = DisableManager(item)
            # item_obj = DisableManager(id_part=item['id_part'], name_part=item['name_part'] , parent_id=item['parent_id'] , status=item['status'] , status_current=item['status_current'] , admin_access=item['admin_access'] , message_disable=item['message_disable'],start_date_disable=item['start_date_disable'] , end_date_disable=item['end_date_disable'] , hidden=item['hidden'] , color=item['color'] , alpha=item['alpha'])
            DisablePartManager.app_list_disable.append(item_obj)
            if item_obj.name_part in disable_acl_map:
                item_disable_acl_map = disable_acl_map[item_obj.name_part]
                DisablePartManager.app_list_disable_str.extend(item_disable_acl_map)
                for item_acl_map in item_disable_acl_map:
                    DisablePartManager.app_dict_disable[item_acl_map] = {'message_disable': item_obj.message_disable, 'url_name': list(item_disable_acl_map), 'hidden': item_obj.hidden, 'color': item_obj.color, 'alpha': item_obj.alpha, 'name_part': item_obj.name_part}
                if not item_obj.admin_access:
                    DisablePartManager.app_list_disable_str_for_admin.extend(disable_acl_map[item_obj.name_part])
            else:
                DisablePartManager.app_list_disable_str.append(item_obj.name_part)
                if not item_obj.admin_access:
                    DisablePartManager.app_list_disable_str_for_admin.append(item_obj.name_part)

        DisablePartManager.date_time_load_list = datetime.datetime.now()

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        if DisablePartManager.date_time_load_list:
            if datetime.datetime.now() - DisablePartManager.date_time_load_list > datetime.timedelta(minutes=10):  # minutes=10): # seconds=1
                DisablePartManager.load_app_list()
        else:
            DisablePartManager.load_app_list()
        # DisablePartManager.load_app_list()

        current_url = resolve(request.path_info).url_name
        if current_url in DisablePartManager.app_list_disable_str:
            try:
                user_type = request.user.userbox.user_type
                user_level = request.user.userbox.user_level
            except:
                auth.logout(request)
                return render(request, "apps/access/login.html")

            is_admin = check_is_admin(user_type, user_level)
            if is_admin and not (current_url in DisablePartManager.app_list_disable_str_for_admin):
                return
            else:
                context = DisablePartManager.app_dict_disable[current_url]
                return page_disable_view(request, context)
        else:
            return


def check_is_admin(user_type, user_level):
    """
    برای بررسی اینکه نوع یوزر ادمین هست یا نه
    :param part_item:
    :param user_type:
    :param user_level:
    :return:
    """
    is_admin = False
    if user_type == 'advisor' or user_type == 'admin':
        is_admin = True
    elif 'country' in user_level:  # TODO بعدا سلکت رول را پاس بدهیم تا بشود بر اساس رولی که انتخاب شده تصمیم گرفت که نشان بدهد یا نه
        is_admin = True
    return is_admin


def get_data_disble_part(url_name):
    pass


def get_user_type(user):
    try:
        if user.baseuser.student:
            return 'student'
    except:
        try:
            if user.baseuser.teacher:
                return 'teacher'
        except:
            try:
                if user.baseuser.advisor:
                    return 'advisor'
            except:
                return 'admin'


def get_user_level(user, user_type=None):
    if not user_type:
        user_type = get_user_type(user)

    if user_type == "student":
        return ["student"]

    if user_type == "teacher":
        levels = []
        db_levels = user.baseuser.teacher.coach_levels.all()
        for item in db_levels:
            if item.level_code == "province":
                if item.show_activity == "both":
                    levels.append(item.level_code)
                    continue

                if item.show_activity == "female":
                    levels.append("province_f")
                    continue

                if item.show_activity == "male":
                    levels.append("province_m")
                    continue

            levels.append(item.level_code)
        return levels

    if user_type == 'advisor':
        levels = []
        db_levels = user.baseuser.advisor.levels.all()
        for item in db_levels:
            levels.append(item.level_code)
        return levels
