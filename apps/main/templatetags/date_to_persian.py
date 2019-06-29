from django import template
import jdatetime
from datetime import datetime
import locale

register = template.Library()


@register.filter(name='date_to_persian')
def date_to_persian(value):
    if value:
        cleaned_value = value
        if value.find(".") != -1:
            cleaned_value = value.split(".")[0]

        datetime_object = datetime.strptime(cleaned_value, '%Y-%m-%dT%H:%M:%S')

        jalali = jdatetime.datetime.fromgregorian(datetime=datetime_object)
        locale.setlocale(locale.LC_ALL, "fa_IR")
        return jalali.strftime("%a, %d %b %Y, %H:%M")
    else:
        return ""


@register.filter(name='date_to_datepicker')
def date_to_datepicker(value, has_time=True):

    cleaned_value = value
    if value.find(".") != -1:
        cleaned_value = value.split(".")[0]
    if has_time:
        datetime_object = datetime.strptime(cleaned_value, '%Y-%m-%dT%H:%M:%S')
    else:
        datetime_object = datetime.strptime(cleaned_value, '%Y-%m-%d')
        jalali = jdatetime.datetime.fromgregorian(datetime=datetime_object)
        locale.setlocale(locale.LC_ALL, "fa_IR")
        return jalali.strftime("%Y/%m/%d")
    jalali = jdatetime.datetime.fromgregorian(datetime=datetime_object)
    locale.setlocale(locale.LC_ALL, "fa_IR")
    return jalali.strftime("%Y/%m/%d %H:%M")
