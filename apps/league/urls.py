from django.conf.urls import url
from apps.league.views import (
    LeagueNewIndex,
    SingleLeagueSchool
)

urlpatterns = [
    url(r'^$', LeagueNewIndex.as_view(), name='league_index'),
    url(r'^(?P<school_id>[\w\d-]+)$', SingleLeagueSchool.as_view(), name='league_single_school'),
]
