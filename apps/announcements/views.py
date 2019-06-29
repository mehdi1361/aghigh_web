import json
import requests
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from apps.announcements.custom_validator import BaseValidator
from apps.announcements.schema import announcements_schema, update_announcements_schema
from apps.main.views import BaseViewClass
from utils.cleandata_pre_post import list_dumps
from apps.main.utils import get_top_level, get_sub_levels, convert_date_milady, set_data_has_access_to_area


class AnnouncementIndex(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/announcements/",
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {})
        )
        self.is_auth_valid(request, get_res)

        announcements = []
        try:
            announcements = get_res.json()
        except:
            pass
        pagination_data = self.return_pagination(response=announcements, page=request.GET.get('page', 1))

        context = {
            "announcements": announcements,
            "pagination_data": pagination_data
        }

        return render(request=request, context=context,
                      template_name="apps/announcements/index.html")


class SingleAnnouncement(BaseViewClass):
    def get(self, request, announcement_id):

        announcement_id = self.decode_id(announcement_id)

        if announcement_id:
            get_res = requests.get(
                url=settings.SERVER_FULL_URL + "/api/v1/announcements/" + str(announcement_id),
                headers=self.get_http_header(request),
            )
            self.is_auth_valid(request, get_res)

            announcement = {}
            try:
                announcement = get_res.json()
            except:
                pass

            if get_res.status_code == 200:
                get_res = requests.get(
                    url=settings.SERVER_FULL_URL + "/api/v1/announcements/" + str(announcement_id) + "/seen",
                    headers=self.get_http_header(request),
                )
                self.is_auth_valid(request, get_res)

                context = {
                    "announcement_item": announcement,
                }

                return render(
                    request=request,
                    context=context,
                    template_name="apps/announcements/single.html"
                )

        else:
            return HttpResponseNotFound()


class MyPostedAnnouncement(BaseViewClass):
    def get(self, request):

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/my_announcements/",
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {})
        )
        self.is_auth_valid(request, get_res)

        announcements = []
        try:
            announcements = get_res.json()
        except:
            pass

        pagination_data = self.return_pagination(response=announcements, page=request.GET.get('page', 1))

        context = {
            "announcements": announcements,
            "pagination_data": pagination_data
        }

        return render(
            request=request,
            context=context,
            template_name="apps/announcements/posted.html"
        )


class DeleteAnnouncement(BaseViewClass):
    def post(self, request, announcement_id):
        announcement_id = self.decode_id(announcement_id)
        if not announcement_id:
            return HttpResponseNotFound()

        get_res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/announcements/" + str(announcement_id) + "/delete_an/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)

        context = {
            'status': get_res.status_code
        }
        return JsonResponse(context)


class UpdateAnnouncement(BaseViewClass):
    def get(self, request, announcement_id, **kwargs):

        announcement_id = self.decode_id(announcement_id)
        if not announcement_id:
            return HttpResponseNotFound()

        top_level = get_top_level(request)
        sub_levels = get_sub_levels(request)

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/announcements/" + str(announcement_id) + "/information",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)

        try:
            data = get_res.json()
            announcement = data['announcement']
            announcement_receivers = data['announcement_receivers']

        except:
            announcement = {}
            announcement_receivers = []

        context = {
            "top_level": top_level,
            "sub_levels": sub_levels,
            'errors': kwargs.get('errors', {}),
            'response': kwargs.get('response', ""),
            'announcement': announcement,
            'update_id': announcement_id,
            'announcement_receivers': announcement_receivers
        }
        set_data_has_access_to_area(context, request, top_level)

        return render(
            request=request,
            context=context,
            template_name="apps/announcements/update.html"
        )

    def post(self, request, announcement_id):
        decode_announcement_id = announcement_id
        announcement_id = self.decode_id(announcement_id)
        if not announcement_id:
            return HttpResponseNotFound()

        headers = self.get_http_header(request)
        post_files, post_req = cleaned_data(request)

        v = BaseValidator(update_announcements_schema())
        v.allow_unknown = True
        if v.validate(post_req):

            _req = self.update_announcement(headers, post_files, list_dumps(post_req=post_req), request, announcement_id)
            try:
                context = {
                    "errors": "" if _req.status_code == 200 else _req.json(),
                    "response": _req.status_code
                }
                return self.get(request, decode_announcement_id, **context)

            except:
                context = {
                    "errors": {"server_error": ["internal_error"]},
                    "response": 500
                }
                return self.get(request, decode_announcement_id, **context)
        else:
            context = {
                "errors": v.errors,
                "response": 400
            }
            return self.get(request, decode_announcement_id, **context)

    def update_announcement(self, headers, post_files, post_req, request, announcement_id):
        _res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/announcements/" + str(announcement_id) + "/update/",
            data=post_req, files=post_files, headers=headers
        )
        self.is_auth_valid(request, _res)
        return _res


class CreateAnnouncement(BaseViewClass):
    def get(self, request, **kwargs):

        top_level = get_top_level(request)
        sub_levels = get_sub_levels(request)

        context = {
            "top_level": top_level,
            "sub_levels": sub_levels,
            'errors': kwargs.get('errors', {}),
            'announcement': kwargs.get('announcement', ''),
        }
        set_data_has_access_to_area(context, request, top_level)

        return render(
            request=request,
            context=context,
            template_name="apps/announcements/submit.html"
        )

    def post(self, request):
        headers = self.get_http_header(request)
        post_files, post_req = cleaned_data(request)

        v = BaseValidator(announcements_schema())
        v.allow_unknown = True
        if v.validate(post_req):

            _req = self.insert_announcement(headers, post_files, list_dumps(post_req=post_req), request)
            try:
                if _req.status_code == 200 or _req.status_code == 201:
                    return redirect('posted_announcement')
                else:
                    errors = {"server_error": ["internal_error"]}
            except:
                errors = {"server_error": ["internal_error"]}

            context = {
                "errors": errors,
                "announcement": post_req
            }
        else:
            context = {
                "errors": v.errors,
                "announcement": post_req
            }
        return self.get(request, **context)

    def insert_announcement(self, headers, post_files, post_req, request):
        _res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/announcements/",
            data=post_req, files=post_files, headers=headers
        )
        self.is_auth_valid(request, _res)
        return _res


def cleaned_data(request):
    release_time = convert_date_milady(request.POST.get("release_time", ""))

    post_req = {
        "title": request.POST.get("title", ""),
        "description": request.POST.get("description", ""),
        "has_date": False if request.POST.get('has_date', 'off') == "off" else True,
        "temp_has_date": request.POST.get("has_date", ""),
        "deleted_image": request.POST.get("deleted_image", ""),
        "release_time": release_time,
        "receivers": json.loads(request.POST.get("receivers", '[]')),
        "deleted_files": json.loads(request.POST.get("deleted_files", '[]')),
        "deleted_receivers": json.loads(request.POST.get("deleted_receivers", '[]'))
    }
    for field in list(post_req):
        if post_req[field] == "":
            post_req.pop(field)

    post_files = []

    image = request.FILES.get("image", None)
    if image:
        post_files.append(('image', image))

    for file_item in request.FILES.getlist("files[]"):
        post_files.append(
            ('files[]', (file_item.name, file_item.file.read(), file_item.content_type))
        )

    return post_files, post_req
