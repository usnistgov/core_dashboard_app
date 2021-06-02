""" Url router for the administration site
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path
from django.urls import reverse_lazy

from core_dashboard_app.views.common import views as dashboard_app_common_views
from core_dashboard_common_app import constants as dashboard_constants
from core_dashboard_common_app.views.common import (
    views as dashboard_common_app_common_views,
)
from core_explore_common_app.views.user import ajax as user_ajax
from core_main_app.views.common.ajax import EditTemplateVersionManagerView

admin_urls = [
    # Admin
    re_path(
        r"^records$",
        staff_member_required(
            dashboard_common_app_common_views.DashboardRecords.as_view(
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_records",
    ),
    re_path(
        r"^forms$",
        staff_member_required(
            dashboard_common_app_common_views.DashboardForms.as_view(
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_forms",
    ),
    re_path(
        r"^dashboard-templates$",
        staff_member_required(
            dashboard_common_app_common_views.DashboardTemplates.as_view(
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_templates",
    ),
    re_path(
        r"^dashboard-types$",
        staff_member_required(
            dashboard_common_app_common_views.DashboardTypes.as_view(
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_types",
    ),
    re_path(
        r"^files$",
        staff_member_required(
            dashboard_common_app_common_views.DashboardFiles.as_view(
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_files",
    ),
    re_path(
        r"^queries$",
        staff_member_required(
            dashboard_common_app_common_views.DashboardQueries.as_view(
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_queries",
    ),
    re_path(
        r"^query/(?P<persistent_query_type>\w+)/(?P<persistent_query_id>\w+)",
        staff_member_required(
            user_ajax.ContentPersistentQueryView.as_view(
                administration=True,
                template="core_explore_common_app/admin/persistent_query/view_query_content.html",
            )
        ),
        name="core_explore_common_persistent_query_content",
    ),
    re_path(
        r"^workspaces$",
        staff_member_required(
            dashboard_common_app_common_views.DashboardWorkspaces.as_view(
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_workspaces",
    ),
    re_path(
        r"^workspace/(?P<workspace_id>\w+)$",
        staff_member_required(
            dashboard_app_common_views.DashboardWorkspaceTabs.as_view(
                administration=True,
                template="core_dashboard_app/admin/my_dashboard_container.html",
            )
        ),
        name="core_dashboard_workspace_list",
    ),
    re_path(
        r"^dashboard-template/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(
            EditTemplateVersionManagerView.as_view(
                success_url=reverse_lazy("admin:core_dashboard_templates")
            )
        ),
        name="core_dashboard_app_edit_template",
    ),
    re_path(
        r"^dashboard-type/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(
            EditTemplateVersionManagerView.as_view(
                success_url=reverse_lazy("admin:core_dashboard_types")
            )
        ),
        name="core_dashboard_app_edit_type",
    ),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
