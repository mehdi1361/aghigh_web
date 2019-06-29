from django.conf.urls import url
from apps.reports.views import (
    DateRegisterActivityReports,
    ActivityReports,
    ActivityProvince,
    UserReports,
    SchoolReports,
    IndexReports,
    AverageActivityTime,
    ActivityCatDep,
    DateDoneActivityReports,
    DateAcceptActivityReports
)

urlpatterns = [
    url(r'^activity/date_register', DateRegisterActivityReports.as_view(), name='date_register_activity_reports'),
    url(r'^$', IndexReports.as_view(), name='index_report'),
    url(r'^activity$', ActivityReports.as_view(), name='activity_reports'),
    url(r'^activity/date_done/$', DateDoneActivityReports.as_view(), name='date_done_activity_reports'),
    url(r'^activity/date_accept/$', DateAcceptActivityReports.as_view(), name='date_accept_activity_reports'),
    url(r'^get_activity_from_province/$', ActivityProvince.as_view(), name='get_activity_from_province'),
    url(r'^average_date_activity_reports/$', AverageActivityTime.as_view(), name='average_date_activity_reports'),
    url(r'^activity_cat_dep/$', ActivityCatDep.as_view(), name='activity_cat_dep'),
    url(r'^user', UserReports.as_view(), name='user_reports'),
    url(r'^school_reports', SchoolReports.as_view(), name='school_reports'),
]