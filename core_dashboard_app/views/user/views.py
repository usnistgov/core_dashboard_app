"""
    Views available for the user
"""

import copy

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

import core_main_app.components.data.api as workspace_data_api
import core_main_app.components.workspace.api as workspace_api
from core_dashboard_app import constants as dashboard_constants
from core_dashboard_app.views.common.forms import UserForm
from core_main_app.components.user import api as user_api
from core_main_app.settings import INSTALLED_APPS
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.rendering import render
from core_main_app.views.user.forms import WorkspaceForm


@login_required(login_url=reverse_lazy("core_main_app_login"))
def dashboard_workspace_records(request, workspace_id):
    """ List the records of a workspace.

    Args:
        request:
    Return:
    """
    workspace = workspace_api.get_by_id(workspace_id)

    try:
        workspace_data = workspace_data_api.get_all_by_workspace(workspace, request.user)
    except AccessControlError, ace:
        workspace_data = []

    number_columns = 5
    detailed_user_data = []
    user_can_read = workspace_api.can_user_read_workspace(workspace, request.user)
    user_can_write = workspace_api.can_user_write_workspace(workspace, request.user)
    for data in workspace_data:
        is_owner = str(data.user_id) == str(request.user.id)
        detailed_user_data.append({'data': data,
                                   'can_read': user_can_read or is_owner,
                                   'can_write': user_can_write or is_owner,
                                   'is_owner': is_owner})

    # Add user_form for change owner
    user_form = UserForm(request.user)
    context = {
        'user_data': detailed_user_data,
        'user_form': user_form,
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.RECORD,
        'template': dashboard_constants.DASHBOARD_RECORDS_TEMPLATE_TABLE_DATATABLE,
        'number_columns': number_columns,
        'administration': False
    }

    # Get all username and corresponding ids
    user_names = dict((str(x.id), x.username) for x in user_api.get_all_users())
    context.update({'usernames': user_names})
    context.update({'title': 'List of records of workspace: ' + workspace.title})

    modals = ["core_main_app/user/workspaces/list/modals/assign_workspace.html"]

    assets = {
        "css": copy.deepcopy(dashboard_constants.CSS_COMMON),

        "js": [{
                    "path": 'core_main_app/user/js/workspaces/list/modals/assign_workspace.js',
                    "is_raw": False
               },
               {
                    "path": 'core_main_app/common/js/backtoprevious.js',
                    "is_raw": True
               },
               {
                    "path": dashboard_constants.USER_VIEW_RECORD_RAW,
                    "is_raw": True
               },
               {
                    "path": dashboard_constants.JS_EDIT_RECORD,
                    "is_raw": False
               },
               {
                    "path": dashboard_constants.JS_VIEW_RECORD,
                    "is_raw": False
               }
        ]
    }

    _handle_asset_modals(assets, modals, delete=True, change_owner=True, menu=False,
                         workspace=workspace.title)

    return render(request, dashboard_constants.DASHBOARD_TEMPLATE,
                  context=context,
                  assets=assets,
                  modals=modals)


@login_required(login_url=reverse_lazy("core_main_app_login"))
def dashboard_workspaces(request):
    """ List the files.

    Args:
        request:
    Return:
    """

    # Get the workspace the user can read
    user_workspace_read = list(workspace_api.get_all_workspaces_with_read_access_by_user(request.user))
    # Get the workspace the user can write
    user_workspace_write = list(workspace_api.get_all_workspaces_with_write_access_by_user(request.user))
    # Get the merged list without doublons
    user_workspaces = user_workspace_read + list(set(user_workspace_write) - set(user_workspace_read))
    detailed_user_workspaces = []
    for user_workspace in user_workspaces:
        detailed_user_workspaces.append({'user': user_api.get_user_by_id(user_workspace.owner).username,
                                         'is_owner': user_workspace.owner == str(request.user.id),
                                         'name': user_workspace.title,
                                         'workspace': user_workspace,
                                         'can_read': user_workspace in user_workspace_read,
                                         'can_write': user_workspace in user_workspace_write,
                                         'is_public': workspace_api.is_workspace_public(user_workspace)
                                         })

    context = {
        'workspace_form': WorkspaceForm(),
        'user_data': detailed_user_workspaces,
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.WORKSPACE,
        'template': dashboard_constants.DASHBOARD_WORKSPACES_TEMPLATE_TABLE,
        'number_columns': 6,
        'create_workspace': True
    }

    modals = ["core_main_app/user/workspaces/list/create_workspace.html",
              "core_main_app/user/workspaces/list/modals/set_public.html"]

    assets = {
        "css": copy.deepcopy(dashboard_constants.CSS_COMMON),

        "js": [{
                    "path": 'core_main_app/user/js/workspaces/create_workspace.js',
                    "is_raw": False
               },
               {
                    "path": 'core_main_app/user/js/workspaces/list/modals/set_public.js',
                    "is_raw": False
               }
        ]
    }

    _handle_asset_modals(assets, modals,
                         delete=True,
                         change_owner=False,
                         menu=False)

    return render(request, dashboard_constants.DASHBOARD_TEMPLATE,
                  context=context,
                  assets=assets,
                  modals=modals)


def _handle_asset_modals(assets, modal, delete=False, change_owner=False, menu=False, workspace=False):
    """ Add needed assets.

    Args:
        assets
        modal
        delete
        change_owner
        menu

    Return:
    """

    # Admin or user assets
    assets['js'].append({
                            "path": dashboard_constants.JS_INIT_USER,
                            "is_raw": True
                       })
    assets['js'].append({
                            "path": dashboard_constants.JS_USER_TABLE,
                            "is_raw": False
                        })
    # Common asset
    assets['js'].extend(dashboard_constants.JS_COMMON)
    if delete:
        assets['js'].append({
                                "path": dashboard_constants.JS_COMMON_FUNCTION_DELETE,
                                "is_raw": False
                             })
        modal.append(dashboard_constants.MODALS_COMMON_DELETE)
    if change_owner:
        assets['js'].append({
                              "path": dashboard_constants.JS_COMMON_FUNCTION_CHANGE_OWNER,
                              "is_raw": False
                            })
        modal.append(dashboard_constants.MODALS_COMMON_CHANGE_OWNER)

    # Menu
    assets['js'].append({
                            "path": dashboard_constants.JS_USER_SELECTED_ELEMENT,
                            "is_raw": True
                        })
