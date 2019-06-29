from django.conf.urls import url
from apps.announcements.views import (
    AnnouncementIndex,
    SingleAnnouncement,
    CreateAnnouncement,
    MyPostedAnnouncement,
    UpdateAnnouncement,
    DeleteAnnouncement,
)


urlpatterns = [
    url(r'^posted$', MyPostedAnnouncement.as_view(), name='posted_announcement'),
    url(r'^create$', CreateAnnouncement.as_view(), name='create_announcement'),
    url(r'^edit/(?P<announcement_id>[\w\d-]+)$', UpdateAnnouncement.as_view(), name='update_announcement'),
    url(r'^delete/(?P<announcement_id>[\w\d-]+)$', DeleteAnnouncement.as_view(), name='delete_announcement'),
    url(r'^(?P<announcement_id>[\w\d-]+)$', SingleAnnouncement.as_view(), name='single_announcement'),
    url(r'^$', AnnouncementIndex.as_view(), name='announcements_index'),
]
