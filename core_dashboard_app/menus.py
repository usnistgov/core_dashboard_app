"""
    User Dashboard menu
"""
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem
from core_dashboard_app.settings import DASHBOARD_MENU, INSTALLED_APPS

for item in DASHBOARD_MENU:
    Menu.add_item(
        "dashboard", MenuItem(item, reverse(DASHBOARD_MENU[item]))
    )

sharing_children = (
    MenuItem("All Records", reverse("admin:core_dashboard_records"), icon="list"),
    MenuItem("All Templates", reverse("admin:core_dashboard_templates"), icon="list"),
    MenuItem("All Files", reverse("admin:core_dashboard_files"), icon="list"),
    MenuItem("All Workspaces", reverse("admin:core_dashboard_workspaces"), icon="list"),
)

if 'core_curate_app' in INSTALLED_APPS:
    sharing_children += (MenuItem("All Forms", reverse("admin:core_dashboard_forms"), icon="list"),)

if 'core_composer_app' in INSTALLED_APPS:
    sharing_children += (MenuItem("All Types", reverse("admin:core_dashboard_types"), icon="list"),)

Menu.add_item(
    "admin", MenuItem("DASHBOARD", None, children=sharing_children)
)
