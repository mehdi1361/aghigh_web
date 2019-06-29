from django import template
from django.conf import settings
import requests

from apps.main.views import BaseViewClass

register = template.Library()


@register.filter
def get_count_notifications(request):
    get_res = requests.get(
        url=settings.SERVER_FULL_URL + "/api/v1/get_notify_count/",
        headers=BaseViewClass.get_http_header(request)
    )
    try:
        count = get_res.json()["count"]
    except:
        count = 0
    return count
