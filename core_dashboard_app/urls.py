""" Url router for the user dashboard
"""
from core_dashboard_app.views import views
from django.conf.urls import url
from core_dashboard_app.views.views import UserDashboardPasswordChangeFormView

urlpatterns = [

    # Common
    url(r'^$', views.home, name='core_dashboard_homepage'),
    url(r'^my-profile$', views.my_profile, name='core_dashboard_profile'),
    url(r'^my-profile/edit$', views.my_profile_edit, name='core_dashboard_profile_edit'),
    url(r'^my-profile/change-password', UserDashboardPasswordChangeFormView.as_view(
        template_name='my_profile_change_password.html', success_url='/'),
        name='core_dashboard_profile_change_password')
]
