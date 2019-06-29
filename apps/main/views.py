import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from utils.request_utils import get_header
from utils.hashids import Hashids


def page_not_found_view(request):
    return render(
        request,
        template_name="apps/main/404.html"
    )


def page_error_view(request):
    return render(
        request,
        template_name="apps/main/500.html"
    )


def page_502_view(request):
    return render(
        request,
        template_name="apps/main/502.html"
    )


def page_permission_denied_view(request):
    if request.method == "post":
        return render(
            request,
            template_name="apps/main/403.html"
        )
    else:
        return render(
            request,
            template_name="apps/main/403.html"
        )
        return HttpResponseForbidden()


def page_disable_view(request, context):
    # if request.method == "post":
    return render(
        request,
        template_name="apps/main/disable_page.html",
        context=context
    )


# else:
#     return HttpResponseForbidden()


def page_bad_request_view(request):
    return render(
        request,
        template_name="apps/main/400.html"
    )


class BaseViewClass(LoginRequiredMixin, View):
    login_url = '/access/login'
    redirect_field_name = 'redirect_to'

    @staticmethod
    def decode_id(item_id):
        try:
            hash_ids = Hashids(min_length=8, salt=settings.SECRET_KEY)
            decoded_id = hash_ids.decode(item_id)
            return decoded_id[0]
        except:
            return None

    @staticmethod
    def encode_id(item_id):
        try:
            hash_ids = Hashids(min_length=8, salt=settings.SECRET_KEY)
            hash_id = hash_ids.encode(item_id)
            return hash_id
        except:
            return None

    @staticmethod
    def get_http_header(request):
        return get_header(request)

    @staticmethod
    def is_auth_valid(request, response):
        # if status_code == 401 or status_code == 403:
        #     auth.logout(request)
        #     return redirect(reverse("access_login"))

        if response.status_code == 401:
            auth.logout(request)
            return redirect(reverse("access_login"))

    @staticmethod
    def return_pagination(response, page=None):
        try:
            pagination_params = ['count', 'next', 'previous']
            for pagination_param in pagination_params:

                if pagination_param not in response:
                    return None
        except:
            return None

        try:
            current_page = int(page) if page else 1
            result_count = response["count"]

            if result_count == 0:
                return None

            if result_count % settings.PAGE_SIZE == 0:
                page_count = result_count // settings.PAGE_SIZE
            else:
                page_count = (result_count // settings.PAGE_SIZE) + 1

            if page_count == 1:
                pagination_data = dict()
                return pagination_data

            list_page = []

            if current_page == page_count:
                if page_count - 2 > 0:
                    list_page.append(page_count - 2)

            if current_page - 1 > 0:
                list_page.append(current_page - 1)

            list_page.append(current_page)

            if current_page + 1 <= page_count:
                list_page.append(current_page + 1)

            if len(list_page) < 3:
                if current_page == 1:
                    if current_page + 2 < page_count:
                        list_page.append(current_page + 2)

                if current_page == page_count - 1:
                    if current_page - 2 > 0:
                        list_page.insert(0, current_page - 2)

            if current_page == page_count - 2:
                list_page.append(page_count)

            last_page_show = False

            if page_count not in list_page:
                if page_count - 1 in list_page:
                    list_page.append(page_count)
                else:
                    last_page_show = True

            first_page_show = False

            if 1 not in list_page:
                if 2 in list_page:
                    list_page.insert(0, 1)
                else:
                    first_page_show = True

            pagination_data = dict(
                page_count=page_count,
                list_page=list_page,
                current_page=current_page,
                has_next=True if current_page + 1 <= page_count else False,
                has_previous=True if current_page - 1 > 0 else False,
                last_page_show=last_page_show,
                first_page_show=first_page_show,
                last_page=page_count,
                first_page=1,
            )

            return pagination_data

        except:
            return None @staticmethod

    @staticmethod
    def add_pagination_param(request, params):

        if params is None:
            params = {}

        page = request.GET.get("page", None)
        if page:
            params["page"] = page
            return params
        return params

    def set_role_gender(self, param):
        if self.request.user.userbox.user_type == "teacher":
            gender_select = self.request.user.userbox.gender_select
            param["gender"] = gender_select if gender_select else self.request.user.userbox.gender_select
            param["role"] = self.request.user.userbox.role_select
        return param


class MainIndex(BaseViewClass):
    def get(self, request):
        context = {}
        if request.user.userbox.user_type == "student":
            context['school_activities'] = self.get_school_last_activity(request)

        context['league_results'] = self.get_top_schools(request)

        context['announcements'] = self.get_announcements(request)

        context['new_activities'] = self.get_new_activities(request)

        context['vip_activities'] = self.get_vip_activities(request)

        return render(
            request,
            context=context,
            template_name="apps/main/index.html"
        )

    def get_new_activities(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v2/activities/search/",
            headers=self.get_http_header(request),
            params=self.set_role_gender({"page": 1})
        )
        self.is_auth_valid(request, get_res)
        if get_res.status_code == 200:
            new_activities = get_res.json()["results"]
        else:
            new_activities = []
        return new_activities

    def get_vip_activities(self, request):
        query_params = {
            "vip": 1,
        }
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v2/activities/search/",
            headers=self.get_http_header(request),
            params=self.set_role_gender(query_params)
        )
        self.is_auth_valid(request, get_res)
        try:
            vip_activities = get_res.json()["results"]
        except:
            vip_activities = []

        return vip_activities

    def get_announcements(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/announcements/",
            headers=self.get_http_header(request),
            params=self.set_role_gender({})
        )
        self.is_auth_valid(request, get_res)
        try:
            announcements = get_res.json()['results'][0:5]
        except:
            announcements = []
        return announcements

    def get_top_schools(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/league/?query_type=top_school",
            headers=self.get_http_header(request),
            params=self.set_role_gender({})
        )
        self.is_auth_valid(request, get_res)
        try:
            league_results = get_res.json()['results'][0:11]
        except:
            league_results = []
        return league_results

    def get_school_last_activity(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/",
            headers=self.get_http_header(request),
            params=self.set_role_gender({})
        )
        self.is_auth_valid(request, get_res)
        school_activities = []
        if get_res.status_code == 200:
            school_activities = get_res.json()["results"][:5]
        return school_activities


class Cities(BaseViewClass):
    def get(self, request, province_id):
        selected_province_id = int(province_id)

        if selected_province_id == 0:
            return []

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/provinces/" + str(selected_province_id) + "/cities/",
            headers=self.get_http_header(request),
            params=self.set_role_gender({})
        )
        self.is_auth_valid(request, get_res)

        context = {
            "cities": get_res.json()
        }

        return JsonResponse(context)


class Camps(BaseViewClass):
    def get(self, request, county_id):
        selected_county_id = int(county_id)

        if selected_county_id == 0:
            return []

        try:
            get_res_camp = requests.get(
                url=settings.SERVER_FULL_URL + "/api/v1/counties/" + str(selected_county_id) + "/camps",
                headers=self.get_http_header(request),
                params=self.set_role_gender({})
            )
            camps = get_res_camp.json()
        except:
            camps = []

        context = {
            "camps": camps
        }

        return JsonResponse(context)


class Schools(BaseViewClass):
    def get(self, request, camp_id):
        selected_camp_id = int(camp_id)

        if selected_camp_id == 0:
            return []

        try:
            get_res = requests.get(
                url=settings.SERVER_FULL_URL + "/api/v1/camps/" + str(selected_camp_id) + "/schools",
                headers=self.get_http_header(request),
                params=self.set_role_gender({})
            )
            schools = get_res.json()
        except:
            schools = []

        context = {
            "schools": schools
        }

        return JsonResponse(context)
