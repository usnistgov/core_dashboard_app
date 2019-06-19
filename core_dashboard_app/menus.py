"""
    User Dashboard menu
"""
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

from core_dashboard_app.settings import INSTALLED_APPS
from core_dashboard_common_app.constants import FUNCTIONAL_OBJECT_ENUM

Menu.add_item(
    "dashboard", MenuItem('{0}s'.format(FUNCTIONAL_OBJECT_ENUM.TEMPLATE.title()), reverse('core_dashboard_templates'))
)

Menu.add_item(
    "dashboard", MenuItem('{0}s'.format(FUNCTIONAL_OBJECT_ENUM.RECORD.title()), reverse('core_dashboard_records'))
)

Menu.add_item(
    "dashboard", MenuItem('{0}s'.format(FUNCTIONAL_OBJECT_ENUM.FILE.title()), reverse('core_dashboard_files'))
)

Menu.add_item(
    "dashboard", MenuItem('{0}s'.format(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.title()), reverse('core_dashboard_workspaces'))
)

sharing_children = (
    MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.RECORD.title()), reverse("admin:core_dashboard_records"),
             icon="list"),
    MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.TEMPLATE.title()), reverse("admin:core_dashboard_templates"),
             icon="list"),
    MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.FILE.title()), reverse("admin:core_dashboard_files"),
             icon="list"),
    MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.title()), reverse("admin:core_dashboard_workspaces"),
             icon="list"),
)

if 'core_composer_app' in INSTALLED_APPS:
    Menu.add_item(
        "dashboard",
        MenuItem('{0}s'.format(FUNCTIONAL_OBJECT_ENUM.TYPE.title()), reverse('core_dashboard_types'))
    )
    sharing_children += (MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.TYPE.title()),
                                  reverse("admin:core_dashboard_types"), icon="list"),)

if 'core_curate_app' in INSTALLED_APPS:
    Menu.add_item(
        "dashboard",
        MenuItem('{0}s'.format(FUNCTIONAL_OBJECT_ENUM.FORM.title()), reverse('core_dashboard_forms'))
    )
    sharing_children += (MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.FORM.title()),
                                  reverse("admin:core_dashboard_forms"), icon="list"),)

Menu.add_item(
    "user", MenuItem("My Profile", reverse('core_dashboard_profile'), icon="user")
)

Menu.add_item(
    "admin", MenuItem("DASHBOARD", None, children=sharing_children)
)
