"""
    Url router for the user dashboard
"""
from django.conf.urls import url

from core_dashboard_app.views.common import ajax, views as common_views
from core_dashboard_app.views.user import views as user_views
from core_dashboard_app.views.common.views import UserDashboardPasswordChangeFormView
from core_main_app.settings import INSTALLED_APPS
from core_main_app.views.user import ajax as workspace_ajax

urlpatterns = [

    # Common
    url(r'^$', common_views.home, name='core_dashboard_home'),
    url(r'^my-profile$', common_views.my_profile, name='core_dashboard_profile'),
    url(r'^my-profile/edit$', common_views.my_profile_edit, name='core_dashboard_profile_edit'),
    url(r'^my-profile/change-password', UserDashboardPasswordChangeFormView.as_view(
        template_name='core_dashboard_app/my_profile_change_password.html', success_url='/'),
        name='core_dashboard_profile_change_password'),

    url(r'^delete-document', ajax.delete_document, name='core_dashboard_delete_document'),
    url(r'^change-owner', ajax.change_owner_document, name='core_dashboard_change_owner_document'),
    url(r'^edit-record', ajax.edit_record, name='core_dashboard_edit_record'),

    # User
    url(r'^records$', user_views.dashboard_records, name='core_dashboard_records'),
    url(r'^forms$', user_views.dashboard_forms, name='core_dashboard_forms'),
    url(r'^templates$', user_views.dashboard_templates, name='core_dashboard_templates'),
    url(r'^types$', user_views.dashboard_types, name='core_dashboard_types'),
    url(r'^files$', user_views.dashboard_files, name='core_dashboard_files'),
    url(r'^workspaces$', user_views.dashboard_workspaces, name='core_dashboard_workspaces'),
    url(r'^workspace-list-records/(?P<workspace_id>\w+)$', user_views.dashboard_workspace_records,
        name='core_dashboard_workspace_list_data')

]
