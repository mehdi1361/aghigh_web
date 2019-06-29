"""aghighweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog

handler404 = 'apps.main.views.page_not_found_view'
handler500 = 'apps.main.views.page_error_view'
handler502 = 'apps.main.views.page_502_view'
handler403 = 'apps.main.views.page_permission_denied_view'
handler400 = 'apps.main.views.page_bad_request_view'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.main.urls')),
    url(r'^activity/', include('apps.activity.urls')),
    url(r'^calendar/', include('apps.calendar_app.urls')),
    url(r'^school/', include('apps.my_school.urls')),
    url(r'^league/', include('apps.league.urls')),
    url(r'^hamraz/', include('apps.hamraz.urls')),
    url(r'^access/', include('apps.access.urls')),
    url(r'^notifications/', include('apps.notification.urls')),
    url(r'^announcements/', include('apps.announcements.urls')),
    url(r'^reports/', include('apps.reports.urls')),
    url(r'^shop/', include('apps.shop.urls')),
    url('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
