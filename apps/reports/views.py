import requests
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.conf import settings
from django.utils.translation import ugettext as _
from apps.main.utils import convert_date_milady
from apps.main.views import BaseViewClass
from utils.date_converter import to_julian


class DateRegisterActivityReports(BaseViewClass):
    def get(self, request):
        report_type = request.GET.get("report_type", "")
        if report_type not in ["hour", "week", "month", "day"]:
            return HttpResponseNotFound()

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/provinces/",
            headers=self.get_http_header(request)
        )
        try:
            provinces = get_res.json()["results"]
        except:
            provinces = []

        self.is_auth_valid(request, get_res)

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_categories/",
            headers=self.get_http_header(request)
        )
        try:
            categories = get_res.json()["results"]
        except:
            categories = []

        self.is_auth_valid(request, get_res)

        params = self.set_params(request)

        reports = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_reports/dateـregister",
            params=params,
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, reports)

        report_title = ""
        axisx_title = ""
        alert_info = ""
        if report_type == "hour":
            report_title = _("date register hour")
            alert_info = _("info date register hour")
            axisx_title = _("hour")
        elif report_type == "week":
            report_title = _("date register week")
            alert_info = _("info date register week")
            axisx_title = ""
        elif report_type == "day":
            report_title = _("date register day")
            alert_info = _("info date register day")
            axisx_title = _("date")
        try:
            reports_data = reports.json()
        except:
            reports_data = []

        context = {
            "provinces": provinces,
            "categories": categories,
            "reports_data": reports_data,
            "query_params": params,
            "report_title": report_title,
            "report_type": report_type,
            "alert_info": alert_info,
            "axisx_title": axisx_title,
        }
        return render(
            request=request,
            template_name="apps/reports/dateregister.html",
            context=context
        )

    def set_params(self, request):
        start_date = convert_date_milady(request.GET.get("start_date", ""), has_time=False)
        end_date = convert_date_milady(request.GET.get("end_date", ""), has_time=False)
        params = dict(
            start_date=start_date,
            end_date=end_date,
            gender=request.GET.get("gender", None),
            province=request.GET.get("province", None),
            county=request.GET.get("county", None),
            camp=request.GET.get("camp", None),
            school=request.GET.get("school", None),
            category=request.GET.get("category", None),
            report_type=request.GET.get("report_type", None)
        )
        return params


class IndexReports(BaseViewClass):
    def get(self, request):
        context = {}

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/reports/last",
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, get_res)
        if get_res.status_code == 200 and get_res.json()["activity_count"]:
            reports = get_res.json()
            context["activity_count"] = reports["activity_count"]
            context["average_difference"] = reports["accept_avg"]
            context["visit_count"] = reports["view_count"]
            context["cache_date"] = reports["created_at"]
            context["active_school_count"] = reports["school_count"]
        else:
            context["activity_count"] = 0
            context["average_difference"] = 0
            context["visit_count"] = 0
            context["cache_date"] = ""
            context["active_school_count"] = 0

        return render(
            request=request,
            template_name="apps/reports/index.html",
            context=context
        )


class UserReports(BaseViewClass):
    def get(self, request):
        context = {
            "message": "error"
        }

        get_provinces = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/provinces/",
            headers=self.get_http_header(request)
        )
        try:
            context["provinces"] = get_provinces.json()["results"]
        except:
            pass

        return render(
            request=request,
            template_name="apps/reports/users.html",
            context=context
        )

    def post(self, request):
        province = request.POST.get("province", "")
        county = request.POST.get("county", "")
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")

        params = {}
        if province.isdigit():
            params["province"] = province

        if county.isdigit():
            params["county"] = county

        if start_date:
            try:
                params["start_date"] = to_julian(start_date)
            except:
                pass

        if end_date:
            try:
                params["end_date"] = to_julian(end_date)
            except:
                pass

        reports = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/user_reports/",
            headers=self.get_http_header(request),
            params=params
        )
        self.is_auth_valid(request, reports)
        context = {
            "message": "error"
        }
        if reports.status_code == 200:
            context["message"] = "success"
            context["data"] = reports.json()
            context["cache_date"] = reports.json()["cache_date"]

        return JsonResponse(context)


class ActivityReports(BaseViewClass):
    def get(self, request):
        reports = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_reports/provinces",
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, reports)
        context = {
            "message": "error"
        }
        if reports.status_code == 200:
            context["message"] = "success"
            context["data_report_province"] = reports.json()

        return render(
            request=request,
            template_name="apps/reports/activities.html",
            context=context
        )


class DateDoneActivityReports(BaseViewClass):
    def get(self, request):

        report_type = request.GET.get("report_type", "")
        if report_type not in ["hour", "week", "month", "day"]:
            return HttpResponseNotFound()

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/provinces/",
            headers=self.get_http_header(request)
        )
        try:
            provinces = get_res.json()["results"]
        except:
            provinces = []

        self.is_auth_valid(request, get_res)

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_categories/",
            headers=self.get_http_header(request)
        )
        try:
            categories = get_res.json()["results"]
        except:
            categories = []

        self.is_auth_valid(request, get_res)

        params = self.set_params(request)

        reports = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_reports/date_done",
            params=params,
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, reports)

        try:
            reports_data = reports.json()
        except:
            reports_data = []

        report_title = ""
        axisx_title = ""
        alert_info = ""
        if report_type == "hour":
            report_title = _("date done hour")
            alert_info = _("info date done hour")
            axisx_title = _("hour")
        elif report_type == "week":
            report_title = _("date done week")
            alert_info = _("info date done week")
            axisx_title = ""
        elif report_type == "day":
            report_title = _("date done day")
            alert_info = _("info date done day")
            axisx_title = _("date")
        context = {
            "provinces": provinces,
            "categories": categories,
            "reports_data": reports_data,
            "query_params": params,
            "report_title": report_title,
            "report_type": report_type,
            "alert_info": alert_info,
            "axisx_title": axisx_title,
        }
        return render(
            request=request,
            template_name="apps/reports/date_done_activities.html",
            context=context
        )

    def set_params(self, request):
        start_date = convert_date_milady(request.GET.get("start_date", ""), has_time=False)
        end_date = convert_date_milady(request.GET.get("end_date", ""), has_time=False)
        params = dict(
            start_date=start_date,
            end_date=end_date,
            gender=request.GET.get("gender", None),
            province=request.GET.get("province", None),
            county=request.GET.get("county", None),
            camp=request.GET.get("camp", None),
            school=request.GET.get("school", None),
            category=request.GET.get("category", None),
            report_type=request.GET.get("report_type", None)
        )
        return params


class DateAcceptActivityReports(BaseViewClass):
    def get(self, request):

        report_type = request.GET.get("report_type", "")
        if report_type not in ["hour", "week", "month", "day"]:
            return HttpResponseNotFound()

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/provinces/",
            headers=self.get_http_header(request)
        )
        try:
            provinces = get_res.json()["results"]
        except:
            provinces = []

        self.is_auth_valid(request, get_res)

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_categories/",
            headers=self.get_http_header(request)
        )
        try:
            categories = get_res.json()["results"]
        except:
            categories = []

        self.is_auth_valid(request, get_res)

        params = self.set_params(request)

        reports = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_reports/date_accept",
            params=params,
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, reports)

        try:
            reports_data = reports.json()
        except:
            reports_data = []

        report_title = ""
        axisx_title = ""
        alert_info = ""
        if report_type == "hour":
            report_title = _("date accept hour")
            alert_info = _("info date accept hour")
            axisx_title = _("hour")
        elif report_type == "week":
            report_title = _("date accept week")
            alert_info = _("info date accept week")
            axisx_title = ""
        elif report_type == "day":
            report_title = _("date accept day")
            alert_info = _("info date accept day")
            axisx_title = _("date")

        context = {
            "provinces": provinces,
            "categories": categories,
            "reports_data": reports_data,
            "query_params": params,
            "report_title": report_title,
            "report_type": report_type,
            "axisx_title": axisx_title,
            "alert_info": alert_info
        }
        return render(
            request=request,
            template_name="apps/reports/date_accept_activities.html",
            context=context
        )

    def set_params(self, request):
        start_date = convert_date_milady(request.GET.get("start_date", ""), has_time=False)
        end_date = convert_date_milady(request.GET.get("end_date", ""), has_time=False)
        params = dict(
            start_date=start_date,
            end_date=end_date,
            gender=request.GET.get("gender", None),
            province=request.GET.get("province", None),
            county=request.GET.get("county", None),
            camp=request.GET.get("camp", None),
            school=request.GET.get("school", None),
            category=request.GET.get("category", None),
            report_type=request.GET.get("report_type", None)
        )
        return params


class ActivityProvince(BaseViewClass):
    def post(self, request):
        reports = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_reports/province",
            headers=self.get_http_header(request),
            params={"code": request.POST.get("code")}
        )
        self.is_auth_valid(request, reports)
        context = {
            "message": "error"
        }
        if reports.status_code == 200:
            context["message"] = "success"
            context["data"] = reports.json()

        return JsonResponse(context)


class AverageActivityTime(BaseViewClass):
    def get(self, request):
        reports = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_reports/average_difference",
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, reports)
        context = {
            "message": "error"
        }
        if reports.status_code == 200:
            context["message"] = "success"
            context["average_accept"] = reports.json()

        return render(
            request=request,
            template_name="apps/reports/activities_average_time.html",
            context=context
        )


class SchoolReports(BaseViewClass):
    def get(self, request):
        gender = request.GET.get("gender", request.user.userbox.gender)

        reports = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/school_reports/province_ranking",
            headers=self.get_http_header(request),
            params={"gender": gender}
        )
        self.is_auth_valid(request, reports)
        context = {
            "message": "error",
            "gender": gender
        }
        if reports.status_code == 200:
            context["message"] = "success"
            context["province_ranking"] = reports.json()

        return render(
            request=request,
            template_name="apps/reports/schools.html",
            context=context
        )


class ActivityCatDep(BaseViewClass):
    def get(self, request):
        param = {}
        context = {}

        gender = request.GET.get("gender", "")
        province = request.GET.get("province", "")
        county = request.GET.get("county", "")

        if gender:
            param["gender"] = gender

        self.get_province(context, request)

        if province.isdigit():
            param["province"] = int(province)
            self.get_county(context, param, request)

        if county.isdigit():
            param["county"] = int(county)

        reports = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_reports/activity_cat_dep",
            headers=self.get_http_header(request),
            params=param
        )
        self.is_auth_valid(request, reports)

        if reports.status_code == 200:
            context["activities"] = reports.json()

        context.update(param)

        return render(
            request=request,
            template_name="apps/reports/activity_cat_dep.html",
            context=context
        )

    def get_county(self, context, param, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/provinces/" + str(param['province']) + "/cities/",
            headers=self.get_http_header(request),
        )
        try:
            context['counties'] = get_res.json()
        except:
            context['counties'] = []

    def get_province(self, context, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/provinces/",
            headers=self.get_http_header(request),
        )
        try:
            context['provinces'] = get_res.json()["results"]
        except:
            context['provinces'] = []
