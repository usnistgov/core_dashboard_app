"""
    Django settings for core_dashboard_app app
"""

# FIXME: case of uninstall app

from django.conf import settings

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, 'SERVER_URI', "http://localhost")

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

# Menu
DASHBOARD_MENU = getattr(settings, 'DASHBOARD_MENU', {
    'My Files': 'core_dashboard_files',
    'My Types': 'core_dashboard_types',
    'My Templates': 'core_dashboard_templates',
    'My Forms': 'core_dashboard_forms',
    'My Records': 'core_dashboard_records',
    'My Profile': 'core_dashboard_profile'
})
