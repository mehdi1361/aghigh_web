# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse

from apps.main.views import BaseViewClass


class LeagueNewIndex(BaseViewClass):
    def get(self, request):

        query_type = request.GET.get("query_type", None)

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/league/",
            headers=self.get_http_header(request),
            params=self.set_role_gender({})
        )
        self.is_auth_valid(request, get_res)

        tabs_json = get_res.json()

        allow_tabs = []
        for tab_item in tabs_json["results"]:
            allow_tabs.append(tab_item["query_type"])

        if not query_type:
            first_item = tabs_json["results"][0]
            query_type = first_item["query_type"]

        if query_type not in allow_tabs:
            return redirect(reverse("league_index"))

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/league/",
            headers=self.get_http_header(request),
            params=self.set_role_gender({"query_type": query_type})
        )

        messages = {}
        league_results = []
        if get_res.status_code == 200:
            league_results = get_res.json()

        context = {
            "tabs": tabs_json,
            "query_type": query_type,
            "league": league_results,
            "messages": messages
        }

        return render(request=request,
                      template_name="apps/league/league.html",
                      context=context)


class SingleLeagueSchool(BaseViewClass):
    def get(self, request, school_id):
        school_id = self.decode_id(school_id)

        if not school_id:
            return HttpResponseNotFound()

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/league/" + str(school_id),
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, get_res)

        if get_res.status_code == 200:

            school_data = get_res.json()

            query_params = dict(
                school=school_id,
                gender=school_data["gender"],
            )

            get_res = requests.get(
                url=settings.SERVER_FULL_URL + "/api/v2/activities/search/",
                headers=self.get_http_header(request),
                params=self.add_pagination_param(request, query_params)
            )
            self.is_auth_valid(request, get_res)

            school_activities = []
            try:
                school_activities = get_res.json()
            except:
                pass

            pagination_data = self.return_pagination(response=school_activities, page=request.GET.get('page', 1))

            context = {
                "school": school_data,
                "pagination_data": pagination_data,
                "school_activities": school_activities,
            }

            return render(request=request, context=context,
                          template_name="apps/league/school.html")

        return HttpResponseNotFound()
