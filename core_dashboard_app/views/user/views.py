"""
    Views available for the user
"""

import copy

import core_main_app.components.data.api as workspace_data_api
import core_main_app.components.version_manager.api as version_manager_api
import core_main_app.components.workspace.api as workspace_api
from core_dashboard_app.views.common.forms import ActionForm, UserForm
from core_main_app.components.blob import api as blob_api, utils as blob_utils
from core_main_app.components.data import api as data_api
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.user import api as user_api
from core_main_app.settings import INSTALLED_APPS
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.rendering import render
from core_main_app.views.user.forms import WorkspaceForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from core_dashboard_app import constants as dashboard_constants
if 'core_composer_app' in INSTALLED_APPS:
    from core_composer_app.components.type_version_manager import api as type_version_manager_api
    from core_composer_app.components.type import api as type_api
if 'core_curate_app' in INSTALLED_APPS:
    import core_curate_app.components.curate_data_structure.api as curate_data_structure_api


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

    number_columns = 4
    detailed_user_data = []
    user_can_read = workspace_api.can_user_read_workspace(workspace, request.user)
    user_can_write = workspace_api.can_user_write_workspace(workspace, request.user)
    for data in workspace_data:
        is_owner = str(data.user_id) == str(request.user.id)
        detailed_user_data.append({'data': data,
                                   'can_read': user_can_read or is_owner,
                                   'can_write': user_can_write or is_owner,
                                   'is_owner': is_owner
                                   })

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
               }]
    }

    assets['js'].extend([{
        "path": 'core_main_app/common/js/backtoprevious.js',
        "is_raw": True
    }])

    assets['js'].extend(copy.deepcopy(dashboard_constants.JS_RECORD))
    assets['js'].extend(copy.deepcopy(dashboard_constants.USER_VIEW_RECORD_RAW))

    _handle_asset_modals(assets, modals, delete=True, change_owner=True, menu=False,
                         workspace=workspace.title)

    return render(request, dashboard_constants.DASHBOARD_TEMPLATE,
                  context=context,
                  assets=assets,
                  modals=modals)


@login_required(login_url=reverse_lazy("core_main_app_login"))
def dashboard_forms(request):
    """ List the forms.

    Args:
         request:

    Return:
    """

    # Get the forms
    forms = curate_data_structure_api.get_all_by_user_id_with_no_data(request.user.id)

    # User Form
    user_form = UserForm(request.user)

    detailed_forms = []
    for form in forms:
        template_name = version_manager_api.get_from_version(form.template).title
        detailed_forms.append({'form': form,
                               'template': template_name})

    context = {'user_data': detailed_forms,
               'user_form': user_form,
               'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FORM,
               'template': dashboard_constants.DASHBOARD_FORMS_TEMPLATE_TABLE
               }

    modals = []

    assets = {
        "css": copy.deepcopy(dashboard_constants.CSS_COMMON),

        "js": []
    }

    _handle_asset_modals(assets, modals, delete=True, change_owner=True, menu=True)

    return render(request, dashboard_constants.DASHBOARD_TEMPLATE,
                  context=context,
                  assets=assets,
                  modals=modals)


@login_required(login_url=reverse_lazy("core_main_app_login"))
def dashboard_templates(request):
    """ List the templates.

    Args:
        request:

    Return:
    """

    # Get user templates
    user_template_versions = template_version_manager_api.get_all_by_user_id(request.user.id)
    detailed_user_template = []
    for user_template_version in user_template_versions:

        detailed_user_template.append({'template_version': user_template_version,
                                       'template': template_api.get(user_template_version.current),
                                       'user': request.user.username,
                                       'title': user_template_version.title
                                       })

    # Add user_form for change owner
    user_form = UserForm(request.user)
    context = {
        'user_data': detailed_user_template,
        'user_form': user_form,
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.TEMPLATE,
        'object_name': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.TEMPLATE,
        'template': dashboard_constants.DASHBOARD_TEMPLATES_TEMPLATE_TABLE
    }

    modals = [
                "core_main_app/admin/templates/list/modals/edit.html",
                "core_main_app/admin/templates/list/modals/disable.html"
            ]

    assets = {
        "css": copy.deepcopy(dashboard_constants.CSS_COMMON),

        "js": [{
                    "path": 'core_main_app/common/js/templates/list/restore.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/common/js/templates/list/modals/edit.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/common/js/templates/list/modals/disable.js',
                    "is_raw": False
                }]
    }

    _handle_asset_modals(assets, modals,
                         delete=False,
                         change_owner=False,
                         menu=True)

    return render(request, dashboard_constants.DASHBOARD_TEMPLATE,
                  context=context,
                  assets=assets,
                  modals=modals)


@login_required(login_url=reverse_lazy("core_main_app_login"))
def dashboard_types(request):
    """ List the types.

    Args:
        request:
    Return:
    """

    # Get user types
    user_type_versions = type_version_manager_api.get_version_managers_by_user(request.user.id)
    detailed_user_type = []
    for user_type_version in user_type_versions:
        detailed_user_type.append({'type_version': user_type_version,
                                   'type': type_api.get(user_type_version.current),
                                   'user': request.user.username,
                                   'title': user_type_version.title})

    # Add user_form for change owner
    user_form = UserForm(request.user)
    context = {
        'user_data': detailed_user_type,
        'user_form': user_form,
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.TYPE,
        'object_name': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.TYPE,
        'template': dashboard_constants.DASHBOARD_TYPES_TEMPLATE_TABLE
    }

    modals = [
                "core_main_app/admin/templates/list/modals/edit.html",
                "core_main_app/admin/templates/list/modals/disable.html"
             ]

    assets = {
        "css": copy.deepcopy(dashboard_constants.CSS_COMMON),

        "js": [{
                    "path": 'core_main_app/common/js/templates/list/restore.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/common/js/templates/list/modals/edit.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/common/js/templates/list/modals/disable.js',
                    "is_raw": False
                }]
    }

    _handle_asset_modals(assets, modals,
                         delete=False,
                         change_owner=False,
                         menu=True)

    return render(request, dashboard_constants.DASHBOARD_TEMPLATE,
                  context=context,
                  assets=assets,
                  modals=modals)


@login_required(login_url=reverse_lazy("core_main_app_login"))
def dashboard_files(request):
    """ List the files.

    Args:
        request:
    Return:
    """
    user_files = blob_api.get_all_by_user_id(request.user.id)
    detailed_user_file = []
    for user_file in user_files:
        detailed_user_file.append({'user': request.user.username,
                                   'date': user_file.id.generation_time,
                                   'file': user_file,
                                   'url': blob_utils.get_blob_download_uri(user_file, request)
                                   })

    context = {
        'user_data': detailed_user_file,
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FILE,
        'template': dashboard_constants.DASHBOARD_FILES_TEMPLATE_TABLE
    }

    modals = []

    assets = {
        "css": copy.deepcopy(dashboard_constants.CSS_COMMON),

        "js": []
    }

    _handle_asset_modals(assets, modals,
                         delete=True,
                         change_owner=False,
                         menu=True)

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
        'number_columns': 5,
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
    assets['js'].extend(dashboard_constants.JS_USER)

    # Common asset
    assets['js'].extend(dashboard_constants.JS_COMMON)
    if delete:
        assets['js'].extend(dashboard_constants.JS_COMMON_FUNCTION_DELETE)
        modal.extend(dashboard_constants.MODALS_COMMON_DELETE)
    if change_owner:
        assets['js'].extend(dashboard_constants.JS_COMMON_FUNCTION_CHANGE_OWNER)
        modal.extend(dashboard_constants.MODALS_COMMON_CHANGE_OWNER)

    # Menu
    assets['js'].extend(dashboard_constants.JS_USER_SELECTED_ELEMENT)
