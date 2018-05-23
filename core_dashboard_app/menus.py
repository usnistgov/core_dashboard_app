"""
    User Dashboard menu
"""
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

from core_dashboard_app.constants import FUNCTIONAL_OBJECT_ENUM
from core_dashboard_app.settings import DASHBOARD_MENU, INSTALLED_APPS

for item in DASHBOARD_MENU:
    Menu.add_item(
        "dashboard", MenuItem(item, reverse(DASHBOARD_MENU[item][0]), weight=DASHBOARD_MENU[item][1])
    )

Menu.add_item(
    "user", MenuItem("My Profile", reverse('core_dashboard_profile'))
)

sharing_children = (
    MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.RECORD.title()), reverse("admin:core_dashboard_records"), icon="list"),
    MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.TEMPLATE.title()), reverse("admin:core_dashboard_templates"), icon="list"),
    MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.FILE.title()), reverse("admin:core_dashboard_files"), icon="list"),
    MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.title()), reverse("admin:core_dashboard_workspaces"), icon="list"),
)

if 'core_curate_app' in INSTALLED_APPS:
    sharing_children += (MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.FORM.title()),
                                  reverse("admin:core_dashboard_forms"), icon="list"),)

if 'core_composer_app' in INSTALLED_APPS:
    sharing_children += (MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.TYPE.title()),
                                  reverse("admin:core_dashboard_types"), icon="list"),)

Menu.add_item(
    "admin", MenuItem("DASHBOARD", None, children=sharing_children)
)
