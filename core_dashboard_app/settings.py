"""
Django settings for core_dashboard_app app.
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, 'SERVER_URI', "http://localhost")

INSTALLED_APPS = (
    'core_main_app',
)

# Menu
DASHBOARD_MENU = getattr(settings, 'DASHBOARD_MENU', None)

# Templates
DASHBOARD_HOME_TEMPLATE = getattr(settings, 'DASHBOARD_HOME_TEMPLATE', None)
DASHBOARD_PROFILE_TEMPLATE = 'my_profile.html'
DASHBOARD_PROFILE_EDIT_TEMPLATE = 'my_profile_edit.html'
