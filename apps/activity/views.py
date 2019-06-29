import requests
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotFound
from apps.main.utils import convert_date_milady
from utils.date_converter import to_jorjean
from apps.main.views import BaseViewClass, MainIndex
from apps.activity.custom_validator import BaseValidator
from apps.activity.schema import activity_create_schema, activity_report_schema


class ActivitySubmit(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_categories/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)
        context = {
            "categories": get_res.json()["results"]
        }
        return render(request=request,
                      template_name="apps/activity/submit.html",
                      context=context)

    def post(self, request):
        headers = self.get_http_header(request).copy()
        post_files, post_req = self.cleaned_data(request)
        if request.POST.get("update_id", False):
            _req = self.update_activity(headers, post_files, post_req, request)
            try:
                errors = json.loads(_req.text) if _req.status_code != 200 else []
            except:
                errors = [{"internal_error": 500}]

            if _req.status_code != 200:
                return UpdateActivity().get(
                    request,
                    activity_id=request.POST.get("update_id"),
                    errors=errors,
                    response=_req.status_code
                )
            else:
                return redirect('my_school_index')
        else:
            v = BaseValidator(activity_create_schema())
            v.allow_unknown = True
            if v.validate(post_req):
                _req = self.insert_activity(headers, post_files, post_req, request)
                try:
                    errors = json.loads(_req.text) if _req.status_code != 200 else []
                except:
                    errors = [{"internal_error": 500}]
                context = {
                    "response": _req.status_code,
                    "activity": post_req if _req.status_code != 201 else "",
                    "errors": errors
                }
            else:
                context = {
                    "response": 401,
                    "activity": post_req,
                    "errors": v.errors
                }

            if context["response"] == 201 or context["response"] == 200:
                return redirect('my_school_index')

            else:
                get_res = requests.get(
                    url=settings.SERVER_FULL_URL + "/api/v1/activity_categories/",
                    headers=self.get_http_header(request)
                )
                context["categories"] = get_res.json()["results"]
                return render(request=request,
                              template_name="apps/activity/submit.html",
                              context=context)

    @staticmethod
    def cleaned_data(request):
        start_date = convert_date_milady(request.POST.get("start_date", ""))
        end_date = convert_date_milady(request.POST.get("end_date", ""))

        post_req = {
            "category": request.POST.get("category", ""),
            "title": request.POST.get("title", ""),
            "location": request.POST.get("location", ""),
            "start_date": start_date,
            "end_date": end_date,
            "description": request.POST.get("description", ""),
            "additional_fields[]": []
        }
        for field in list(post_req):
            if post_req[field] == "":
                post_req.pop(field)

        additional_fields = []
        for post_item in request.POST:
            if str(post_item).lower().find("additional_fields") > -1:
                additional_fields.append({
                    "id": int(post_item.split('additional_fields')[-1]), "value": request.POST.get(post_item)
                })
        post_req["additional_fields[]"] = json.dumps(additional_fields)

        post_files = []
        for file_item in request.FILES.getlist("images[]"):
            post_files.append(
                ('images[]', (file_item.name, file_item.file.read(), file_item.content_type))
            )
        for file_item in request.FILES.getlist("files[]"):
            post_files.append(
                ('files[]', (file_item.name, file_item.file.read(), file_item.content_type))
            )

        for key in request.FILES.keys():
            if key.startswith("additional"):
                for file_item in request.FILES.getlist(key):
                    post_files.append(
                        (key, (file_item.name, file_item.file.read(), file_item.content_type))
                    )
        return post_files, post_req

    def insert_activity(self, headers, post_files, post_req, request):
        _res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/",
            data=post_req, files=post_files, headers=headers
        )
        self.is_auth_valid(request, _res)
        return _res

    def update_activity(self, headers, post_files, post_req, request):
        deleted_images = []
        deleted_files = []
        deleted_additional_files = []
        activity_id = self.decode_id(request.POST.get('update_id'))

        if not activity_id:
            return False

        for _id in request.POST.get("deleted_images", '').split(','):
            try:
                deleted_images.append(int(_id))
            except:
                continue
        for _id in request.POST.get("deleted_files", '').split(','):
            try:
                deleted_files.append(int(_id))
            except:
                continue

        for _id in request.POST.get("deleted_additional_files", '').split(','):
            try:
                deleted_additional_files.append(int(_id))
            except:
                continue

        post_req["deleted_images"] = json.dumps(deleted_images)
        post_req["deleted_files"] = json.dumps(deleted_files)
        post_req["deleted_additional_files"] = json.dumps(deleted_additional_files)
        _res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(activity_id) + "/update/",
            data=post_req, files=post_files, headers=headers
        )
        self.is_auth_valid(request, _res)
        return _res


class ActivityIndex(BaseViewClass):
    def get(self, request):
        emtiaz_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/emtiaz",
            headers=self.get_http_header(request),
            params=self.set_role_gender({})
        )
        self.is_auth_valid(request, emtiaz_res)

        try:
            emtiaz_data = emtiaz_res.json()["results"]
        except:
            emtiaz_data = []

        vip_activities = self.get_vip_activities(request)

        special_filters_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/emtiaz/special_filters",
            headers=self.get_http_header(request),
            params=self.set_role_gender({})
        )
        self.is_auth_valid(request, emtiaz_res)
        special_filters = []
        try:
            special_filter = special_filters_res.json()
            special_filters.extend(special_filter['activity'])
            special_filters.extend(special_filter['personal'])
        except:
            pass

        context = {
            "emtiaz": emtiaz_data,
            "special_filters": special_filters,
            "vip_activities": vip_activities
        }

        return render(
            request=request,
            context=context,
            template_name="apps/activity/index.html"
        )

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


class SearchActivity(BaseViewClass):
    def get(self, request):

        points = request.GET.get("point", None)
        order = request.GET.get("order", None)
        county = request.GET.get("county", None)
        text = request.GET.get("text", None)
        province = request.GET.get("province", None)
        my_school = request.GET.get("my_school", None)
        random = request.GET.get("random", None)
        most_view = request.GET.get("most_view", None)
        category = request.GET.get("category", None)

        params = dict(
            county=county,
            random=random,
            most_view=most_view,
            text=text,
            order=order,
            province=province,
            category=category,
            my_school=1 if my_school == "1" else 0,
        )

        if points:
            point_data = points.split(",")
            params["point_start"] = int(float(point_data[0]))
            params["point_end"] = int(float(point_data[1]))

        query_params = {}

        for key in params:
            if params[key] is not None and params[key] is not '':
                query_params[key] = params[key]

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v2/activities/search/",
            headers=self.get_http_header(request),
            params=self.set_role_gender(self.add_pagination_param(request, query_params))
        )
        self.is_auth_valid(request, get_res)
        try:
            activity_resp = get_res.json()
        except:
            activity_resp = []
        pagination_data = self.return_pagination(response=activity_resp, page=request.GET.get('page', 1))

        get_provinces = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/provinces/",
            headers=self.get_http_header(request)
        )
        try:
            provinces = get_provinces.json()["results"]
        except:
            provinces = []

        self.is_auth_valid(request, get_provinces)

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_categories/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)

        context = {
            "activities": activity_resp,
            "pagination_data": pagination_data,
            "provinces": provinces,
            "categories": get_res.json()["results"],
            "query_params": params
        }

        return render(request=request, context=context,
                      template_name="apps/activity/search.html")


class SingleActivity(BaseViewClass):
    def get(self, request, activity_id):
        activity_id = self.decode_id(activity_id)
        if not activity_id:
            return HttpResponseNotFound()

        activity_year = request.GET.get('activity_year')
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(activity_id),
            params={'activity_year': activity_year},
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)

        if get_res.status_code != 200:
            return HttpResponseNotFound()

        activity_data = get_res.json()
        activity_category_id = activity_data["category"]["id"]

        comments_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_comment/" + str(activity_id) + "/activity",
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, params={"activity_year": activity_year})
        )
        self.is_auth_valid(request, comments_res)
        try:
            comments = comments_res.json()
            pagination_data = self.return_pagination(response=comments, page=request.GET.get('page', 1))
            comments = comments['results']

        except:
            comments = []
            pagination_data = {}

        additional_fields_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_categories/" + str(activity_category_id) + "/show_additional_fields/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)

        groups = additional_fields_res.json()["results"]

        groups = make_additional_fields(activity_data["additional_field"], groups)

        params_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/params/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)

        _params = []
        try:
            _params = params_res.json()["results"]
        except:
            pass

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/categories_reports/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)

        categories_reports = []
        try:
            categories_reports = get_res.json()["results"]
        except:
            pass

        context = {
            "activity": activity_data,
            "comments": comments,
            "groups": groups,
            "params": _params,
            "pagination_data": pagination_data,
            "categories_reports": categories_reports
        }

        return render(
            request=request,
            context=context,
            template_name="apps/activity/single.html"
        )


class ChangeStateActivity(BaseViewClass):
    def post(self, request, activity_id):
        context = {"success": False}

        activity_id = self.decode_id(activity_id)
        if not activity_id:
            return HttpResponseNotFound()

        _res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(activity_id) + "/change_state/",
            data={"state": request.POST.get('state', '')}, headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, _res)

        if _res.status_code == 200:
            context['success'] = True

        return JsonResponse(
            data=context
        )


class TestActivity(BaseViewClass):
    def get(self, request):
        return render(
            request=request,
            context={},
            template_name="apps/activity/single_test.html"
        )


class UpdateActivity(BaseViewClass):
    def get(self, request, activity_id, errors=None, response=None):
        activity_id = self.decode_id(activity_id)

        if not activity_id:
            return HttpResponseNotFound()

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(activity_id),
            headers=self.get_http_header(request)
        )

        if get_res.status_code == 200:
            self.is_auth_valid(request, get_res)
            activity = get_res.json()
            # if activity["state"] == "SHE" and activity["student"]["id"] == request.user.userbox.api_user_id:
            # if activity["state"] == "SHE" and activity["student"]["id"] == request.user.userbox.api_user_id:
            activity["start_date"] = to_jorjean(activity.get('start_date', ""))
            activity["end_date"] = to_jorjean(activity.get('end_date', ""))
            activity_list = []
            for item in activity.get('additional_field', "[]"):
                if item['field_type'] == "file_upload":
                    item['value'] = json.loads(item['value'])
                    item['text_value'] = json.loads(item['text_value'])
                activity_list.append(item)

            activity["additional_field"] = json.dumps(activity_list)

            get_res = requests.get(
                url=settings.SERVER_FULL_URL + "/api/v1/activity_categories/",
                headers=self.get_http_header(request)
            )
            self.is_auth_valid(request, get_res)
            categories = get_res.json()["results"]

            context = {
                "activity": activity,
                "errors": errors,
                "response": response,
                "perm": True,
                "categories": categories
            }
            return render(request=request, context=context, template_name="apps/activity/update.html")
            # return render(request=request, context={"perm": False}, template_name="apps/activity/update.html")
        elif get_res.status_code == 403:  # برای نمایش فعالیت رد شده توسط مربی به دانش آموز جدید یک مدرسه
            return render(request=request, context={"perm": False}, template_name="apps/activity/update.html")
        return HttpResponseNotFound()


class AdditionalFields(BaseViewClass):
    def get(self, request, category_id):
        selected_category_id = int(category_id)

        if selected_category_id == 0:
            return []

        groups = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activity_categories/" + str(
                selected_category_id) + "/additional_fields/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, groups)

        context = {
            "groups": groups.json()["results"]
        }

        return JsonResponse(context)


class SubForm(BaseViewClass):
    def get(self, request, sub_form_id):
        selected_sub_form_id = int(sub_form_id)

        if selected_sub_form_id == 0:
            return []

        groups = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v2/activity_categories/" + str(
                selected_sub_form_id) + "/get_sub_form/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, groups)

        context = {
            "groups": groups.json()["results"]
        }

        return JsonResponse(context)


class SendComment(BaseViewClass):
    def post(self, request, activity_id):

        activity_id = self.decode_id(activity_id)

        if not activity_id:
            return JsonResponse({})

        comment = json.loads(request.POST["data"])

        post_data = dict(
            activity=activity_id,
            comment=comment["comment"],
            params=json.dumps(comment["params"])
        )

        comment_url = settings.SERVER_FULL_URL + "/api/v1/activity_comment/"

        comment_method = 'POST'
        if comment["edit_comment_id"]:
            if str(comment["edit_comment_id"]).isdigit():
                if int(comment["edit_comment_id"]) >= 1:
                    comment_url += comment["edit_comment_id"] + '/'
                    comment_method = 'PUT'

        get_res = requests.request(
            method=comment_method,
            url=comment_url,
            headers=self.get_http_header(request),
            data=post_data
        )
        self.is_auth_valid(request, get_res)

        context = {
            "response": get_res.json()
        }

        return JsonResponse(context)


class LikeActivity(BaseViewClass):
    def get(self, request, activity_id):
        selected_activity_id = int(activity_id)

        if selected_activity_id == 0:
            return []

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(selected_activity_id) + "/like",
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, get_res)

        context = {
            "response": get_res.json()
        }

        return JsonResponse(context)


class RateActivity(BaseViewClass):
    def post(self, request):

        context = {
            "message": "error"
        }

        rate = request.POST.get("rate")
        activity_id = request.POST.get("activity_id")

        activity_id = self.decode_id(activity_id)
        if not activity_id:
            return JsonResponse(context)

        rates = ['1', '2', '3', '4', '5']
        if rate in rates and activity_id:
            get_res = requests.post(
                url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(activity_id) + "/rate/",
                headers=self.get_http_header(request),
                data={"rate": rate},
            )
            self.is_auth_valid(request, get_res)
            if get_res.status_code == 200:
                context["message"] = "success"
                context["data"] = get_res.json()

        return JsonResponse(context)


class RateUsersActivity(BaseViewClass):
    def get(self, request, activity_id):

        activity_id = self.decode_id(activity_id)
        if not activity_id:
            return HttpResponseNotFound()

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(activity_id) + "/rate_users/",
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, params=None)
        )
        self.is_auth_valid(request, get_res)
        try:
            rate_info_list = get_res.json()
            pagination_data = self.return_pagination(response=rate_info_list, page=request.GET.get('page', 1))
            rate_info_list = rate_info_list['results']
        except:
            rate_info_list = []
            pagination_data = {}

        return render(
            request=request,
            context={"rate_info_list": rate_info_list, "pagination_data": pagination_data},
            template_name="apps/activity/rate_users.html"
        )

    def post(self, request, activity_id):

        context = {
            "message": "error"
        }

        activity_id = self.decode_id(activity_id)
        if not activity_id:
            return JsonResponse(context)

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(activity_id) + "/rate_users/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)
        if get_res.status_code == 200:
            context["message"] = "success"
            data = []
            for item in get_res.json()['results']:
                data.append({
                    "name": item['student']['first_name'] + " " + item['student']['last_name'],
                    "school_id": self.encode_id(item['student']['school']['id']),
                    "rate": item['rate']
                })
            context["data"] = data

        return JsonResponse(context)


class WorkSpace(BaseViewClass):
    def get(self, request):
        page_name = request.GET.get("page_name", "workspace")

        query_params = {}
        if page_name == "history":
            query_params = {'history': 1}

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/",
            headers=self.get_http_header(request),
            params=self.set_role_gender(self.add_pagination_param(request, query_params))
        )
        self.is_auth_valid(request, get_res)

        try:
            activity_resp = get_res.json()
        except:
            activity_resp = []

        pagination_data = self.return_pagination(response=activity_resp, page=request.GET.get('page', 1))

        context = {
            "activities": activity_resp,
            "show_states": True,
            "pagination_data": pagination_data,
            "page_name": page_name,
            "query_params": query_params
        }

        return render(
            request=request,
            context=context,
            template_name="apps/activity/workspace.html"
        )


class CheckActivity(BaseViewClass):
    def get(self, request, activity_id, errors=None, response=None):
        activity_id = self.decode_id(activity_id)

        if not activity_id:
            return HttpResponseNotFound()

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(activity_id),
            headers=self.get_http_header(request)
        )
        if get_res.status_code == 200:
            self.is_auth_valid(request, get_res)
            activity = get_res.json()
            if activity["state"] == "SHR" or activity["state"] == "NEW":
                activity["start_date"] = to_jorjean(activity.get('start_date', ""))
                activity["end_date"] = to_jorjean(activity.get('end_date', ""))
                activity_list = []
                for item in activity.get('additional_field', "[]"):
                    if item['field_type'] == "file_upload":
                        item['value'] = json.loads(item['value'])
                        item['text_value'] = json.loads(item['text_value'])
                    activity_list.append(item)
                activity["additional_field"] = json.dumps(activity_list)

                get_res = requests.get(
                    url=settings.SERVER_FULL_URL + "/api/v1/activity_categories/",
                    headers=self.get_http_header(request)
                )
                self.is_auth_valid(request, get_res)
                categories = get_res.json()["results"]

                context = {
                    "activity": activity,
                    "errors": errors,
                    "response": response,
                    "perm": True,
                    "categories": categories
                }
                return render(request=request, context=context, template_name="apps/activity/check.html")
            return render(request=request, context={"perm": False}, template_name="apps/activity/check.html")
        return HttpResponseNotFound()

    def post(self, request, activity_id):
        activity_id = self.decode_id(activity_id)

        if not activity_id:
            return HttpResponse(
                json.dumps({'message': 'error'}),
                content_type="application/json"
            )

        data = request.POST.get("data_check_activity")

        try:
            clean_data = clean_data_check_activity(json.loads(data))
        except:
            return HttpResponse(
                json.dumps({'message': 'error'}),
                content_type="application/json"
            )

        get_res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(activity_id) + "/check/",
            headers=self.get_http_header(request),
            data={"data": json.dumps(clean_data)}
        )

        if get_res.status_code == 200:
            return HttpResponse(
                json.dumps({'message': 'success'}),
                content_type="application/json"
            )

        return HttpResponse(
            json.dumps({'message': 'error'}),
            content_type="application/json"
        )


class ConfirmActivity(BaseViewClass):
    def post(self, request, activity_id):
        activity_id = self.decode_id(activity_id)

        if not activity_id:
            return HttpResponse(
                json.dumps({'message': 'error'}),
                content_type="application/json"
            )

        get_res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/activities/" + str(activity_id) + "/confirm/",
            headers=self.get_http_header(request)
        )

        if get_res.status_code == 200:
            return HttpResponse(
                json.dumps({'message': 'success'}),
                content_type="application/json"
            )

        return HttpResponse(
            json.dumps({'message': 'error'}),
            content_type="application/json"
        )


class SpecificActivity(BaseViewClass):
    def get(self, request):

        category = request.GET.get("category", None)
        department = request.GET.get("department", None)
        action = request.GET.get("action", None)

        params = dict(
            category=category,
            action=action,
            department=department,
        )

        query_params = {}
        for key in params:
            if params[key] is not None and params[key] is not '':
                query_params[key] = params[key]

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/emtiaz/specific_activity",
            headers=self.get_http_header(request),
            params=self.set_role_gender(query_params)
        )
        self.is_auth_valid(request, get_res)

        try:
            activity_resp = get_res.json()
        except:
            activity_resp = []

        context = {
            "activities": activity_resp,
        }

        return render(
            request=request,
            context=context,
            template_name="apps/activity/specific_activity.html"
        )


class SpecificStudent(BaseViewClass):
    def get(self, request):

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/emtiaz/specific_student",
            headers=self.get_http_header(request),
            params=self.set_role_gender({})
        )
        self.is_auth_valid(request, get_res)

        try:
            students = get_res.json()
        except:
            students = []

        context = {
            "students": students,
        }

        return render(
            request=request,
            context=context,
            template_name="apps/activity/specific_student.html"
        )


class StudentPoint(BaseViewClass):
    def get(self, request):
        context = {
            "message": "error"
        }

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/emtiaz/student_point",
            headers=self.get_http_header(request),
            params=self.set_role_gender({})
        )
        self.is_auth_valid(request, get_res)

        if get_res.status_code == 200:
            get_res = get_res.json()
            context['data'] = get_res['student_point']
            context['message'] = "success"

        return JsonResponse(context)


class ActivityReportAbuse(BaseViewClass):
    def post(self, request):
        activity_id = request.POST.get("activity_id", "")
        activity_id = self.decode_id(activity_id)
        if not activity_id:
            return HttpResponseNotFound()

        headers = self.get_http_header(request).copy()
        post_req = self.cleaned_data(request)
        post_req['activity'] = str(activity_id)

        v = BaseValidator(activity_report_schema())
        v.allow_unknown = True
        if v.validate(post_req):
            _req = self.insert_activity_report(headers, post_req, request)
            try:
                errors = json.loads(_req.text) if _req.status_code != 201 else []
            except:
                errors = [{"internal_error": 500}]
            context = {
                "response": _req.status_code,
                "errors": errors
            }
        else:
            context = {
                "response": 400,
                "errors": v.errors
            }
        return JsonResponse(
            data=context
        )

    @staticmethod
    def cleaned_data(request):

        post_req = {
            "category": request.POST.get("category_id", ""),
            "content": request.POST.get("content", "")
        }
        for field in list(post_req):
            if post_req[field] == "":
                post_req.pop(field)

        return post_req

    def insert_activity_report(self, headers, post_req, request):
        _res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/report_abuses/",
            data=post_req, headers=headers
        )
        self.is_auth_valid(request, _res)
        return _res


class AllReportAbuse(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/report_abuses/",
            headers=self.get_http_header(request),
            params=self.set_role_gender({"page": request.GET.get("page", 1)})
        )
        self.is_auth_valid(request, get_res)

        report_abuses = []
        pagination_data = {}

        try:
            report_abuses = get_res.json()
            pagination_data = self.return_pagination(response=report_abuses, page=request.GET.get('page', 1))
            report_abuses = get_res.json()["results"]
        except:
            pass

        context = {
            "report_abuses": report_abuses,
            "pagination_data": pagination_data
        }

        return render(
            request=request,
            context=context,
            template_name="apps/activity/all_report_abuse.html"
        )


class OneReportAbuse(BaseViewClass):
    def get(self, request, activity_id):
        activity_id = self.decode_id(activity_id)
        if not activity_id:
            return HttpResponseNotFound()

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/report_abuses/" + str(activity_id),
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, get_res)

        try:
            data = get_res.json()
        except:
            data = {}

        return render(
            request=request,
            context=data,
            template_name="apps/activity/get_report_abuses.html"
        )


def clean_data_check_activity(data):
    generals = data["general"]
    images = data["image"]
    files = data["file"]
    additional_fields = data["additional_field"]
    additional_files = data["additional_files"]
    clean_data = {
        'images': [],
        'files': [],
        'additional_field': [],
        'additional_files': []
    }

    for image in images:
        clean_data["images"].append({
            "id": int(image["id"]),
            "status": bool(image["status"]),
            "comment": str(image["comment"]),
        })

    for file in files:
        clean_data["files"].append({
            "id": int(file["id"]),
            "status": bool(file["status"]),
            "comment": str(file["comment"]),
        })

    for filed in additional_fields:
        clean_data["additional_field"].append({
            "id": int(filed["id"]),
            "status": bool(filed["status"]),
            "comment": str(filed["comment"]),
        })

    for file in additional_files:
        clean_data["additional_files"].append({
            "id": int(file["id"]),
            "status": bool(file["status"]),
            "comment": str(file["comment"]),
        })

    append_general_field_check(clean_data, generals)

    return clean_data


def append_general_field_check(clean_data, generals):
    for item in generals:

        if item['id'] == 'title':
            clean_data['title_status'] = bool(item['status'])
            clean_data['title_comment'] = item["comment"]
            continue

        if item['id'] == 'location':
            clean_data['location_status'] = bool(item['status'])
            clean_data['location_comment'] = item["comment"]
            continue

        if item['id'] == 'start_date':
            clean_data['start_date_status'] = bool(item['status'])
            clean_data['start_date_comment'] = item["comment"]
            continue

        if item['id'] == 'end_date':
            clean_data['end_date_status'] = bool(item['status'])
            clean_data['end_date_comment'] = item["comment"]
            continue

        if item['id'] == 'description':
            clean_data['description_status'] = bool(item['status'])
            clean_data['description_comment'] = item["comment"]
            continue

        if item['id'] == 'category':
            clean_data['category_status'] = bool(item['status'])
            clean_data['category_comment'] = item["comment"]
            continue

        if item['id'] == 'general_comment':
            clean_data['general_comment'] = item["comment"]
            continue


def calculate_point(points):
    final_points = dict(
        param1_point=0,
        param2_point=0,
        param3_point=0,
        param4_point=0,
    )

    for point_item in points:
        final_points["param1_point"] += point_item["param1_point"]
        final_points["param2_point"] += point_item["param2_point"]
        final_points["param3_point"] += point_item["param3_point"]
        final_points["param4_point"] += point_item["param4_point"]

    if final_points["param1_point"] > 0:
        final_points["param1_point"] = point_item["param1_point"] / 5

    if final_points["param2_point"] > 0:
        final_points["param2_point"] = point_item["param2_point"] / 5

    if final_points["param3_point"] > 0:
        final_points["param3_point"] = point_item["param3_point"] / 5

    if final_points["param4_point"] > 0:
        final_points["param4_point"] = point_item["param4_point"] / 5

    return final_points


def find_value(list_items, item_id, key_field):
    for item in list_items:
        if item[key_field] == item_id:
            return item["value"]


def make_additional_fields(activity_additional_field, group_category_additional_fields):
    new_groups = []
    for group in group_category_additional_fields:
        _group = {
            'id': group["id"],
            'label': group["label"]
        }
        _additional_fields = []
        for act_item in activity_additional_field:
            for additional_field in group["additional_fields"]:
                if act_item["additional_field"] == additional_field["id"]:
                    field_value = act_item["value"]

                    try:
                        if additional_field["field_type"] == "drop_down":
                            field_value = find_value(additional_field["values"], int(field_value), "id")
                    except:
                        pass

                    try:
                        if additional_field["field_type"] == "file_upload":
                            # get dict for type file from files_value key
                            additional_field["files"].append(act_item['files_value'])
                            continue
                    except:
                        additional_field["files"] = [act_item['files_value']]

                    additional_field["value"] = field_value

                    if field_value != "" and field_value != "None" and field_value is not None:
                        _additional_fields.append(additional_field)
        if _additional_fields:
            _group["additional_fields"] = _additional_fields
            new_groups.append(_group)

    return new_groups
