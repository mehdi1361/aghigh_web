import json
import requests

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

from apps.main.views import BaseViewClass


class NotificationIndex(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/notify",
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {})
        )
        self.is_auth_valid(request, get_res)

        try:
            notifications = get_res.json()
        except:
            notifications = {}

        if "results" in notifications:
            for notify in notifications["results"]:
                if notify["body_action"]:
                    try:
                        notify["body_action"] = json.loads(notify["body_action"])
                    except:
                        continue

        pagination_data = self.return_pagination(response=notifications, page=request.GET.get('page', 1))

        context = {
            "notifications": notifications,
            "pagination_data": pagination_data
        }

        return render(request=request, context=context,
                      template_name="apps/notification/index.html")

    def post(self, request):
        notify_id = request.POST.get("notify_id")
        if notify_id:
            get_res = requests.post(
                url=settings.SERVER_FULL_URL + "/api/v1/notify/" + notify_id + "/read/",
                headers=self.get_http_header(request),
                params={}
            )
            self.is_auth_valid(request, get_res)

        return JsonResponse({})

