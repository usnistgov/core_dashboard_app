"""
Url router for the administration site
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse_lazy

from core_dashboard_common_app import constants as dashboard_constants
from core_main_app.views.common.ajax import EditTemplateVersionManagerView
from core_dashboard_common_app.views.admin import views as admin_views
from core_dashboard_common_app.views.common import views as common_views

admin_urls = [
    # Admin
    url(r'^records$', staff_member_required(common_views.DashboardRecords.as_view(
        administration=True,
        template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE)),
        name='core_dashboard_records'),
    url(r'^forms$', staff_member_required(common_views.DashboardForms.as_view(
        administration=True,
        template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE)),
        name='core_dashboard_forms'),
    url(r'^dashboard-templates$', staff_member_required(common_views.DashboardTemplates.as_view(
        administration=True,
        template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE)),
        name='core_dashboard_templates'),
    url(r'^dashboard-types$', staff_member_required(common_views.DashboardTypes.as_view(
        administration=True,
        template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE)),
        name='core_dashboard_types'),
    url(r'^files$', staff_member_required(common_views.DashboardFiles.as_view(
        administration=True,
        template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE)),
        name='core_dashboard_files'),
    url(r'^workspaces$', staff_member_required(common_views.DashboardWorkspaces.as_view(
        administration=True,
        template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE)), name='core_dashboard_workspaces'),
    url(r'^workspace-list-records/(?P<workspace_id>\w+)$', admin_views.dashboard_workspace_records,
        name='core_dashboard_workspace_list_data'),
    url(r'^dashboard-template/(?P<pk>[\w-]+)/edit/$',
        EditTemplateVersionManagerView.as_view(success_url=reverse_lazy(
            "admin:core_dashboard_templates")),
        name='core_dashboard_app_edit_template'),
    url(r'^dashboard-type/(?P<pk>[\w-]+)/edit/$',
        EditTemplateVersionManagerView.as_view(success_url=reverse_lazy(
            "admin:core_dashboard_types")),
        name='core_dashboard_app_edit_type'),
]


urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
