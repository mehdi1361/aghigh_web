from django.conf.urls import url
from apps.notification.views import (
    NotificationIndex,
)

urlpatterns = [
    url(r'^$', NotificationIndex.as_view(), name='notification_index'),
]
