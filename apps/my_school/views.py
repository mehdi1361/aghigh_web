import requests
from apps.main.utils import get_top_level
from django.shortcuts import render
from django.conf import settings
from apps.main.views import BaseViewClass
from apps.main.utils import set_data_has_access_to_area


# Create your views here.
class MySchoolIndex(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v2/activities/my_school/",
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {'activity_year': request.GET.get('activity_year')})
        )
        self.is_auth_valid(request, get_res)
        activities = []
        if get_res.status_code == 200:
            activities = get_res.json()

        school_id = request.user.userbox.school_id

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/league/" + str(school_id),
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)

        school_data = []

        try:
            school_data = get_res.json()
        except:
            pass

        pagination_data = self.return_pagination(response=activities, page=request.GET.get('page', 1))

        context = {
            "activities": activities,
            "show_states": True,
            "activity_year": request.GET.get('activity_year'),
            "pagination_data": pagination_data,
            "school": school_data,
        }

        return render(request=request, context=context, template_name="apps/my_school/student.html")


class MySchoolsIndex(BaseViewClass):
    def get(self, request):
        top_level = get_top_level(request) if not request.user.userbox.role_select else request.user.userbox.role_select

        context = {"schools": []}

        param = {}

        if top_level == "country":
            try:
                get_res = requests.get(
                    url=settings.SERVER_FULL_URL + "/api/v1/provinces/",
                    headers=self.get_http_header(request),
                )
                context['provinces'] = get_res.json()["results"]

            except:
                context['provinces'] = []

            try:
                param['province'] = int(request.GET.get('province'))
            except:
                pass

            try:
                get_res = requests.get(
                    url=settings.SERVER_FULL_URL + "/api/v1/provinces/" + str(param['province']) + "/cities/",
                    headers=self.get_http_header(request),
                )
                context['counties'] = get_res.json()

            except:
                context['counties'] = []

            try:
                param['county'] = int(request.GET.get('county'))
            except:
                pass

            try:
                get_res_camp = requests.get(
                    url=settings.SERVER_FULL_URL + "/api/v1/counties/" + str(param['county']) + "/camps",
                    headers=self.get_http_header(request),
                )
                context['camps'] = get_res_camp.json()
            except:
                context['camps'] = []

            try:
                param['camp'] = request.GET.get('camp')
            except:
                pass

        elif top_level == "province" or top_level == "province_f" or top_level == "province_m":
            get_res = requests.get(
                url=settings.SERVER_FULL_URL + "/api/v1/counties/",
                headers=self.get_http_header(request),
            )

            try:
                context['counties'] = get_res.json()
            except:
                context['counties'] = []

            try:
                param['county'] = int(request.GET.get('county'))
            except:
                pass

            try:
                get_res_camp = requests.get(
                    url=settings.SERVER_FULL_URL + "/api/v1/counties/" + str(param['county']) + "/camps",
                    headers=self.get_http_header(request),
                )
                context['camps'] = get_res_camp.json()
            except:
                context['camps'] = []

            try:
                param['camp'] = request.GET.get('camp')
            except:
                pass

        elif top_level == "county":
            get_res = requests.get(
                url=settings.SERVER_FULL_URL + "/api/v1/camps/",
                headers=self.get_http_header(request),
            )

            try:
                context['camps'] = get_res.json()
            except:
                context['camps'] = []

            try:
                param['camp'] = request.GET.get('camp')
            except:
                pass

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/teacher_schools/",
            headers=self.get_http_header(request),
            params=self.set_role_gender(self.add_pagination_param(request, param))
        )

        try:
            context['schools'] = get_res.json()
        except:
            pass

        context['top_level'] = top_level

        pagination_data = self.return_pagination(response=context["schools"], page=request.GET.get('page', 1))

        context['pagination_data'] = pagination_data

        context.update(param)

        self.is_auth_valid(request, get_res)

        return render(
            request=request,
            context=context,
            template_name="apps/my_school/teachers.html"
        )