"""
    Url router for the user dashboard
"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from core_dashboard_common_app.views.common import ajax, views as common_views
from core_dashboard_common_app.views.common.views import UserDashboardPasswordChangeFormView
from core_dashboard_common_app.views.user import views as user_views
from core_main_app.views.common.ajax import EditTemplateVersionManagerView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [

    # Common
    url(r'^$', common_views.home, name='core_dashboard_home'),
    url(r'^my-profile$', common_views.my_profile, name='core_dashboard_profile'),
    url(r'^my-profile/edit$', common_views.my_profile_edit, name='core_dashboard_profile_edit'),
    url(r'^my-profile/change-password', UserDashboardPasswordChangeFormView.as_view(
        template_name='core_dashboard_common_app/my_profile_change_password.html', success_url='/'),
        name='core_dashboard_profile_change_password'),

    url(r'^delete-document', ajax.delete_document, name='core_dashboard_delete_document'),
    url(r'^change-owner', ajax.change_owner_document, name='core_dashboard_change_owner_document'),
    url(r'^edit-record', ajax.edit_record, name='core_dashboard_edit_record'),

    # User
    url(r'^records$', login_required(common_views.DashboardRecords.as_view()), name='core_dashboard_records'),
    url(r'^forms$', login_required(common_views.DashboardForms.as_view()), name='core_dashboard_forms'),
    url(r'^templates$', login_required(common_views.DashboardTemplates.as_view()), name='core_dashboard_templates'),
    url(r'^types$',login_required(common_views.DashboardTypes.as_view()), name='core_dashboard_types'),
    url(r'^files$', login_required(common_views.DashboardFiles.as_view()), name='core_dashboard_files'),
    url(r'^workspaces$', login_required(common_views.DashboardWorkspaces.as_view(
    ), login_url=reverse_lazy("core_main_app_login")), name='core_dashboard_workspaces'),
    url(r'^workspace-list-records/(?P<workspace_id>\w+)$', user_views.dashboard_workspace_records,
        name='core_dashboard_workspace_list_data'),
    url(r'^template/(?P<pk>[\w-]+)/edit/$',
        EditTemplateVersionManagerView.as_view(success_url=reverse_lazy("core_dashboard_templates")),
        name='core_dashboard_app_edit_template'),
    url(r'^type/(?P<pk>[\w-]+)/edit/$',
        EditTemplateVersionManagerView.as_view(success_url=reverse_lazy("core_dashboard_types")),
        name='core_dashboard_app_edit_type'),
]
