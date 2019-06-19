from django.conf.urls import url, include
from django.contrib import admin

from core_dashboard_app import urls as core_dashboard_app_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
] + core_dashboard_app_urls.urlpatterns
