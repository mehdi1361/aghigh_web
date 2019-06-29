from django.conf.urls import url
from apps.my_school.views import MySchoolIndex, MySchoolsIndex

urlpatterns = [
    url(r'^$', MySchoolIndex.as_view(), name='my_school_index'),
    url(r'^teacher$', MySchoolsIndex.as_view(), name='teacher_schools'),
]
