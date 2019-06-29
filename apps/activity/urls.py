from django.conf.urls import url
from apps.activity.views import (
    ActivitySubmit,
    ActivityIndex,
    AdditionalFields,
    SingleActivity,
    UpdateActivity,
    SearchActivity,
    SendComment,
    RateActivity,
    RateUsersActivity,
    LikeActivity,
    CheckActivity,
    SpecificActivity,
    SpecificStudent,
    WorkSpace,
    StudentPoint,
    ActivityReportAbuse,
    OneReportAbuse,
    TestActivity,
    AllReportAbuse,
    ConfirmActivity,
    SubForm,
    ChangeStateActivity
)

urlpatterns = [
    url(r'^$', ActivityIndex.as_view(), name='activity_index'),

    url(r'^submit$', ActivitySubmit.as_view(), name='activity_submit'),
    url(r'^additional_fields/(?P<category_id>[\w\d-]+)$', AdditionalFields.as_view(), name='activity_additional_fields'),
    url(r'^get_sub_form/(?P<sub_form_id>[\w\d-]+)$', SubForm.as_view(), name='get_sub_form'),
    url(r'^comment/(?P<activity_id>[\w\d-]+)$', SendComment.as_view(), name='activity_comment'),
    url(r'^like/(?P<activity_id>[\w\d-]+)$', LikeActivity.as_view(), name='activity_like'),
    url(r'^update/(?P<activity_id>[\w\d-]+)$', UpdateActivity.as_view(), name='activity_update'),
    url(r'^rate/$', RateActivity.as_view(), name='activity_rate'),
    url(r'^users_rate/(?P<activity_id>[\w\d-]+)$', RateUsersActivity.as_view(), name='activity_rate_users'),

    url(r'^search/$', SearchActivity.as_view(), name='search_activity'),
    url(r'^specific/$', SpecificActivity.as_view(), name='specific_activity'),
    url(r'^specific_student/$', SpecificStudent.as_view(), name='specific_student'),
    url(r'^student_point/$', StudentPoint.as_view(), name='student_point'),

    url(r'^workspace/$', WorkSpace.as_view(), name='workspace_index'),
    url(r'^check/(?P<activity_id>[\w\d-]+)$', CheckActivity.as_view(), name='activity_check'),
    url(r'^confirm/(?P<activity_id>[\w\d-]+)$', ConfirmActivity.as_view(), name='activity_confirm'),

    url(r'^(?P<activity_id>[\w\d-]+)$', SingleActivity.as_view(), name='single_activity'),
    url(r'^test_activity/$', TestActivity.as_view(), name='test_activity'),

    url(r'^(?P<activity_id>[\w\d-]+)/change_state$', ChangeStateActivity.as_view(), name='change_state_activity'),

    url(r'^report_abuses/$', ActivityReportAbuse.as_view(), name='activity_report_abuses'),

    url(r'^all_report_abuses/$', AllReportAbuse.as_view(), name='all_report_abuses'),
    url(r'^all_report_abuses/(?P<activity_id>[\w\d-]+)$', OneReportAbuse.as_view(), name='get_report_abuses'),

]
