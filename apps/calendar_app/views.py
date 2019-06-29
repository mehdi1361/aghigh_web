import json
import requests
import datetime
import re
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from apps.main.utils import convert_date_milady
from apps.main.views import BaseViewClass
from apps.calendar_app import static


class CalendarIndex(BaseViewClass):

    def get(self, request):
        context = {
            "repeat_type": static.REPEAT_TYPE,
        }
        today = datetime.datetime.today()
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/annual_events/",
            headers=self.get_http_header(request),
            params={"date": str(today.year) + "," + str(today.month) + "," + str(today.day)}
        )
        self.is_auth_valid(request, get_res)
        if get_res.status_code == 200:
            context["message"] = "success"
            context["annual_events"] = get_res.json()["results"]

        return render(
            request=request,
            context=context,
            template_name="apps/calendar_app/index.html"
        )


class RemoveOccurrence(BaseViewClass):

    def post(self, request):
        occurrence_id = request.POST.get('occurrence_id')
        context = {
            "message": "error"
        }
        if occurrence_id:
            get_res = requests.post(
                url=settings.SERVER_FULL_URL + "/api/v1/occurrence/delete/",
                headers=self.get_http_header(request),
                data={
                    "occurrence_id": occurrence_id
                }
            )
            self.is_auth_valid(request, get_res)
            if get_res.status_code == 200:
                context["message"] = "success"

        return JsonResponse(context)


class RemoveEvent(BaseViewClass):

    def post(self, request):
        event_id = request.POST.get('event_id')
        context = {
            "message": "error"
        }
        if event_id:
            get_res = requests.post(
                url=settings.SERVER_FULL_URL + "/api/v1/event/delete/",
                headers=self.get_http_header(request),
                data={"event_id": event_id}
            )
            self.is_auth_valid(request, get_res)
            if get_res.status_code == 200:
                context["message"] = "success"

        return JsonResponse(context)


class UpdateOccurrence(BaseViewClass):

    def post(self, request):
        context = {
            "message": "error"
        }
        data = {}
        try:
            event = json.loads(request.POST.get("event"))
            event_id = event["event_id"]
            occurrence_id = event["id"]
            end = event["end"]
            start = event["start"]

            data['start'], data['end'] = self.set_date(start, end)
            data['all_day'] = event["allDay"]
            data["occurrence_id"] = occurrence_id
            data["event_id"] = event_id

            data["occurrence_id"] = occurrence_id
            data["event_id"] = event_id
        except:
            try:
                data["occurrence_id"] = request.POST["occurrence_id"]
                data["event_id"] = request.POST["event_id"]
            except:
                return JsonResponse(context)

        cancelled = request.POST.get('cancelled')
        if cancelled:
            dict_bool = {"true": True, "false": False}
            data["cancelled"] = dict_bool.get(cancelled)

        get_res = requests.post(
            url=settings.SERVER_FULL_URL + "/api/v1/occurrence/update/",
            headers=self.get_http_header(request),
            json=data,
        )

        self.is_auth_valid(request, get_res)
        if get_res.status_code == 200:
            context["message"] = "success"

        return JsonResponse(context)

    @staticmethod
    def set_date(start, end):
        try:
            try:
                start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                start = None

            try:
                end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                end = None

            start = str(start).replace(" ", "T")
            end = str(end).replace(" ", "T")

            return start, end

        except:
            return None, None


class GetAnnualEvent(BaseViewClass):
    def post(self, request):
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')
        context = {
            "message": "error"
        }
        if year and month and day:
            get_res = requests.get(
                url=settings.SERVER_FULL_URL + "/api/v1/annual_events/",
                headers=self.get_http_header(request),
                params={"date": year + "," + month + "," + day}
            )
            self.is_auth_valid(request, get_res)
            if get_res.status_code == 200:
                context["message"] = "success"
                context["events"] = get_res.json()["results"]

        return JsonResponse(context)


class Occurrence(BaseViewClass):
    def get(self, request):
        start_date = convert_fa_numbers(request.GET.get("start", ""))
        end_date = convert_fa_numbers(request.GET.get("end", ""))
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/event/",
            headers=self.get_http_header(request),
            params={"end_date": end_date, "start_date": start_date}
        )
        self.is_auth_valid(request, get_res)
        if get_res.status_code == 200:
            context = get_res.json()

        else:
            context = []

        for event in context:
            event["allDay"] = event.pop('all_day')
            event["id_href"] = self.encode_id(event.pop('id_href'))

        return JsonResponse(context, safe=False)

    def post(self, request):

        start_date = convert_date_milady(request.POST.get("start_date", ""), False)
        end_recurring_period = convert_date_milady(request.POST.get("end_recurring_period", ""), False)

        start_time = request.POST.get("start_time", "")
        end_time = request.POST.get("end_time", "")

        title = request.POST.get('title')
        color = request.POST.get('color', "#e91e63")
        description = request.POST.get('description')
        rule = request.POST.get('rule')
        week_days = request.POST.get('week_days')

        f_week_days = []
        if week_days:
            for day in week_days.split(","):
                if day and static.WEEKLY_DAYS.get(day):
                    f_week_days.append(static.WEEKLY_DAYS[day])

        context = {
            "message": "error"
        }

        if start_date and title:
            get_res = requests.post(
                url=settings.SERVER_FULL_URL + "/api/v1/event/",
                headers=self.get_http_header(request),
                json={
                    "start": start_date,
                    "title": title,
                    "color_event": color,
                    "description": description,
                    "start_time": self.set_time(start_time),
                    "end_time": self.set_time(end_time),
                    "week_days": list(f_week_days),
                    "rule": rule,
                    "end_recurring_period": end_recurring_period,
                }
            )
            self.is_auth_valid(request, get_res)
            if get_res.status_code == 201:
                context["message"] = "success"

            elif get_res.status_code == 400:
                context["message"] = "exceeded_limit"

        return JsonResponse(context)

    @staticmethod
    def set_time(str_time):
        if str_time:
            if len(str_time) == 1:
                str_time = "0" + str_time
            str_time = str_time + ":00"
        return str_time


def convert_fa_numbers(input_str):
    """
    This function convert Persian numbers to English numbers.

    Keyword arguments:
    input_str -- It should be string
    Returns: English numbers
    """
    mapping = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
        '.': '.',
    }
    return _multiple_replace(mapping, input_str)


def _multiple_replace(mapping, text):
    """
    Internal function for replace all mapping keys for a input string
    :param mapping: replacing mapping keys
    :param text: user input string
    :return: New string with converted mapping keys to values
    """
    pattern = "|".join(map(re.escape, mapping.keys()))
    return re.sub(pattern, lambda m: mapping[m.group()], str(text))
