"""
    Url router for the user dashboard
"""

from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path
from core_main_app.admin import core_admin_site

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^core-admin/", core_admin_site.urls),
    re_path(r"^", include("core_main_app.urls")),
    re_path(r"^", include("core_curate_app.urls")),
    re_path(r"^", include("core_dashboard_app.urls")),
]
