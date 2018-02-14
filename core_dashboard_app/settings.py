"""
    Django settings for core_dashboard_app app
"""

from django.conf import settings

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, 'SERVER_URI', "http://localhost")

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

menu = {
    'My Templates': ('core_dashboard_templates', 1000),
    'My Records': ('core_dashboard_records', 2000),
    'My Files': ('core_dashboard_files', 3000),
    'My Workspaces': ('core_dashboard_workspaces', 4000),
}

if 'core_composer_app' in INSTALLED_APPS:
    menu['My Types'] = ('core_dashboard_types', 1500)
if 'core_curate_app' in INSTALLED_APPS:
    menu['My Forms'] = ('core_dashboard_forms', 2500)

# Menu
DASHBOARD_MENU = getattr(settings, 'DASHBOARD_MENU', menu)

# Number of records to display per page for pagination
RECORD_PER_PAGE_PAGINATION = getattr(settings, 'RESULTS_PER_PAGE', 10)
