"""
    Django settings for core_dashboard_app app
"""

from django.conf import settings

from core_dashboard_app.constants import FUNCTIONAL_OBJECT_ENUM

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, 'SERVER_URI', "http://localhost")

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

menu = {
    '{0}s'.format(FUNCTIONAL_OBJECT_ENUM.TEMPLATE.title()): ('core_dashboard_templates', 1000),
    '{0}s'.format(FUNCTIONAL_OBJECT_ENUM.RECORD.title()): ('core_dashboard_records', 2000),
    '{0}s'.format(FUNCTIONAL_OBJECT_ENUM.FILE.title()): ('core_dashboard_files', 3000),
    '{0}s'.format(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.title()): ('core_dashboard_workspaces', 4000),
}

if 'core_composer_app' in INSTALLED_APPS:
    menu['{0}s'.format(FUNCTIONAL_OBJECT_ENUM.TYPE.title())] = ('core_dashboard_types', 1500)
if 'core_curate_app' in INSTALLED_APPS:
    menu['{0}s'.format(FUNCTIONAL_OBJECT_ENUM.FORM.title())] = ('core_dashboard_forms', 2500)

# Menu
DASHBOARD_MENU = getattr(settings, 'DASHBOARD_MENU', menu)
