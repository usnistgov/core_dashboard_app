"""
    Url router for the user dashboard
"""
from django.contrib.auth.decorators import login_required
from django.urls import re_path
from django.urls import reverse_lazy

from core_dashboard_app.views.common import views as dashboard_app_common_views
from core_dashboard_common_app.views.common import (
    ajax,
    views as dashboard_common_app_common_views,
)
from core_dashboard_common_app.views.common.views import (
    UserDashboardPasswordChangeFormView,
)
from core_main_app.settings import INSTALLED_APPS
from core_main_app.views.common.ajax import EditTemplateVersionManagerView

urlpatterns = [
    # Common
    re_path(
        r"^$",
        dashboard_common_app_common_views.home,
        name="core_dashboard_home",
    ),
    re_path(
        r"^my-profile$",
        dashboard_common_app_common_views.my_profile,
        name="core_dashboard_profile",
    ),
    re_path(
        r"^my-profile/edit$",
        dashboard_common_app_common_views.my_profile_edit,
        name="core_dashboard_profile_edit",
    ),
    re_path(
        r"^my-profile/change-password",
        UserDashboardPasswordChangeFormView.as_view(
            template_name="core_dashboard_common_app/my_profile_change_password.html",
            success_url="/",
        ),
        name="core_dashboard_profile_change_password",
    ),
    re_path(
        r"^delete-document",
        ajax.delete_document,
        name="core_dashboard_delete_document",
    ),
    re_path(
        r"^change-owner",
        ajax.change_owner_document,
        name="core_dashboard_change_owner_document",
    ),
    re_path(
        r"^edit-record", ajax.edit_record, name="core_dashboard_edit_record"
    ),
    # User
    re_path(
        r"^records$",
        login_required(
            dashboard_common_app_common_views.DashboardRecords.as_view(),
        ),
        name="core_dashboard_records",
    ),
    re_path(
        r"^forms$",
        login_required(
            dashboard_common_app_common_views.DashboardForms.as_view(),
        ),
        name="core_dashboard_forms",
    ),
    re_path(
        r"^templates$",
        login_required(
            dashboard_common_app_common_views.DashboardTemplates.as_view(),
        ),
        name="core_dashboard_templates",
    ),
    re_path(
        r"^types$",
        login_required(
            dashboard_common_app_common_views.DashboardTypes.as_view(),
        ),
        name="core_dashboard_types",
    ),
    re_path(
        r"^files$",
        login_required(
            dashboard_common_app_common_views.DashboardFiles.as_view(),
        ),
        name="core_dashboard_files",
    ),
    re_path(
        r"^queries$",
        login_required(
            dashboard_common_app_common_views.DashboardQueries.as_view(),
        ),
        name="core_dashboard_queries",
    ),
    re_path(
        r"^workspaces$",
        login_required(
            dashboard_common_app_common_views.DashboardWorkspaces.as_view(),
        ),
        name="core_dashboard_workspaces",
    ),
    re_path(
        r"^workspace/(?P<workspace_id>\w+)$",
        login_required(
            dashboard_app_common_views.DashboardWorkspaceTabs.as_view(),
        ),
        name="core_dashboard_workspace_list",
    ),
    re_path(
        r"^template/(?P<pk>[\w-]+)/edit/$",
        EditTemplateVersionManagerView.as_view(
            success_url=reverse_lazy("core_dashboard_templates")
        ),
        name="core_dashboard_app_edit_template",
    ),
]


if "core_composer_app" in INSTALLED_APPS:
    from core_composer_app.views.user.ajax import EditTypeVersionManagerView

    urlpatterns.append(
        re_path(
            r"^type/(?P<pk>[\w-]+)/edit/$",
            EditTypeVersionManagerView.as_view(
                success_url=reverse_lazy("core_dashboard_types")
            ),
            name="core_dashboard_app_edit_type",
        ),
    )
