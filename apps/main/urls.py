from django.conf.urls import url
from apps.main.views import MainIndex, Cities, Camps, Schools

urlpatterns = [
    url(r'^$', MainIndex.as_view(), name='main_index'),
    url(r'^cities/(?P<province_id>[\w\d-]+)$', Cities.as_view(), name='main_cities'),
    url(r'^camps/(?P<county_id>[\w\d-]+)$', Camps.as_view(), name='main_camps'),
    url(r'^schools/(?P<camp_id>[\w\d-]+)$', Schools.as_view(), name='main_schools'),

]
