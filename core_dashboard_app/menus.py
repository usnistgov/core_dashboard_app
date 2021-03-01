"""
    User Dashboard menu
"""
from django.urls import reverse
from menu import Menu, MenuItem

from core_dashboard_app.settings import INSTALLED_APPS
from core_dashboard_common_app.constants import FUNCTIONAL_OBJECT_ENUM
from core_dashboard_common_app.templatetags.special_plural import special_case_plural

Menu.add_item(
    "dashboard",
    MenuItem(
        f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.TEMPLATE.value.title())}",
        reverse("core_dashboard_templates"),
    ),
)

Menu.add_item(
    "dashboard",
    MenuItem(
        f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.RECORD.value.title())}",
        reverse("core_dashboard_records"),
    ),
)

Menu.add_item(
    "dashboard",
    MenuItem(
        f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.FILE.value.title())}",
        reverse("core_dashboard_files"),
    ),
)
Menu.add_item(
    "dashboard",
    MenuItem(
        f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.QUERY.value.title())}",
        reverse("core_dashboard_queries"),
    ),
)

Menu.add_item(
    "dashboard",
    MenuItem(
        f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.value.title())}",
        reverse("core_dashboard_workspaces"),
    ),
)

sharing_children = (
    MenuItem(
        f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.RECORD.value.title())}",
        reverse("admin:core_dashboard_records"),
        icon="list",
    ),
    MenuItem(
        f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.TEMPLATE.value.title())}",
        reverse("admin:core_dashboard_templates"),
        icon="list",
    ),
    MenuItem(
        f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.FILE.value.title())}",
        reverse("admin:core_dashboard_files"),
        icon="list",
    ),
    MenuItem(
        f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.QUERY.value.title())}",
        reverse("admin:core_dashboard_queries"),
        icon="list",
    ),
    MenuItem(
        f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.value.title())}",
        reverse("admin:core_dashboard_workspaces"),
        icon="list",
    ),
)

if "core_composer_app" in INSTALLED_APPS:
    Menu.add_item(
        "dashboard",
        MenuItem(
            f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.TYPE.value.title())}",
            reverse("core_dashboard_types"),
        ),
    )
    sharing_children += (
        MenuItem(
            f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.TYPE.value.title())}",
            reverse("admin:core_dashboard_types"),
            icon="list",
        ),
    )

if "core_curate_app" in INSTALLED_APPS:
    Menu.add_item(
        "dashboard",
        MenuItem(
            f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.FORM.value.title())}",
            reverse("core_dashboard_forms"),
        ),
    )
    sharing_children += (
        MenuItem(
            f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.FORM.value.title())}",
            reverse("admin:core_dashboard_forms"),
            icon="list",
        ),
    )

Menu.add_item(
    "user", MenuItem("My Profile", reverse("core_dashboard_profile"), icon="user")
)

Menu.add_item("admin", MenuItem("DASHBOARD", None, children=sharing_children))
