from django.conf.urls import url
from apps.calendar_app.views import (
    CalendarIndex,
    GetAnnualEvent,
    Occurrence,
    RemoveOccurrence,
    RemoveEvent,
    UpdateOccurrence
)

urlpatterns = [
    url(r'^$', CalendarIndex.as_view(), name='calendar_index'),
    url(r'^get_annual_events/$', GetAnnualEvent.as_view(), name='get_annual_events'),
    url(r'^occurrence/$', Occurrence.as_view(), name='occurrence'),
    url(r'^remove_occurrence/$', RemoveOccurrence.as_view(), name='remove_occurrence'),
    url(r'^remove_event/$', RemoveEvent.as_view(), name='remove_event'),
    url(r'^update_occurrence/$', UpdateOccurrence.as_view(), name='update_occurrence'),
]
