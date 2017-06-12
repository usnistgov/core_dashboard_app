"""
    User Dashboard menu
"""
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem
from core_dashboard_app.settings import DASHBOARD_MENU


for item in DASHBOARD_MENU:
    Menu.add_item(
        "dashboard", MenuItem(item, reverse(DASHBOARD_MENU[item]))
    )
