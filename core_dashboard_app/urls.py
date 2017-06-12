"""
    Url router for the user dashboard
"""
from core_dashboard_app.views import views
from core_dashboard_app.views import ajax
from django.conf.urls import url
from core_dashboard_app.views.views import UserDashboardPasswordChangeFormView

urlpatterns = [

    # Common
    url(r'^$', views.home, name='core_dashboard_home'),
    url(r'^my-profile$', views.my_profile, name='core_dashboard_profile'),
    url(r'^my-profile/edit$', views.my_profile_edit, name='core_dashboard_profile_edit'),
    url(r'^my-profile/change-password', UserDashboardPasswordChangeFormView.as_view(
        template_name='core_dashboard_app/my_profile_change_password.html', success_url='/'),
        name='core_dashboard_profile_change_password'),
    url(r'^records$', views.dashboard_records, name='core_dashboard_records'),
    url(r'^forms$', views.dashboard_forms, name='core_dashboard_forms'),
    url(r'^templates$', views.dashboard_templates, name='core_dashboard_templates'),


    url(r'^delete-document', ajax.delete_document, name='core_dashboard_delete_document'),
    url(r'^change-owner', ajax.change_owner_document, name='core_dashboard_change_owner_document'),
    url(r'^edit-record', ajax.edit_record, name='core_dashboard_edit_record')

]
