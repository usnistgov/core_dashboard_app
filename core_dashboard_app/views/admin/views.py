"""
    Views available for the user
"""

import copy

import core_main_app.components.data.api as workspace_data_api
import core_main_app.components.version_manager.api as version_manager_api
import core_main_app.components.workspace.api as workspace_api
from core_dashboard_app.views.common.forms import ActionForm, UserForm
from core_main_app.components.blob import api as blob_api, utils as blob_utils
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.user import api as user_api
from core_main_app.settings import INSTALLED_APPS
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.rendering import admin_render
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

    detailed_user_data = []
    user_can_read = workspace_api.can_user_read_workspace(workspace, request.user)
    user_can_write = workspace_api.can_user_write_workspace(workspace, request.user)
    for data in workspace_data:
        detailed_user_data.append({'data': data,
                                   'can_read': user_can_read,
                                   'can_write': user_can_write,
                                   'is_owner': True
                                   })

    # Add user_form for change owner
    user_form = UserForm(request.user)
    context = {
        'other_users_data': detailed_user_data,
        'user_form': user_form,
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.RECORD,
        'template': dashboard_constants.DASHBOARD_RECORDS_TEMPLATE_TABLE_DATATABLE,
        'number_columns': 4,
        'administration': True
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
                    "path": dashboard_constants.ADMIN_VIEW_RECORD_RAW,
                    "is_raw": True
               },
               {
                    "path": 'core_main_app/common/js/backtoprevious.js',
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

    return admin_render(request, dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
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

    # User Form
    user_form = UserForm(request.user)

    context = {'user_form': user_form,
               'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FORM,
               'template': dashboard_constants.DASHBOARD_FORMS_TEMPLATE_TABLE
               }

    # Get all username and corresponding ids
    user_names = dict((str(x.id), x.username) for x in user_api.get_all_users())

    # Get all forms from other users
    other_user_forms = curate_data_structure_api.get_all_with_no_data()

    other_detailed_forms = []
    for form in other_user_forms:
        template_name = version_manager_api.get_from_version(form.template).title
        other_detailed_forms.append({'form': form,
                                     'template': template_name})

    context.update({'other_users_data': other_detailed_forms,
                    'usernames': user_names,
                    'number_columns': 5,
                    'action_form': ActionForm(
                        [('1', 'Delete selected forms'), ('2', 'Change owner of selected forms')]),
                    'menu': True})

    modals = []

    assets = {
        "css": copy.deepcopy(dashboard_constants.CSS_COMMON),

        "js": []
    }

    _handle_asset_modals(assets, modals, delete=True, change_owner=True, menu=True)

    return admin_render(request, dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
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

    # Add user_form for change owner
    user_form = UserForm(request.user)
    context = {
        'user_form': user_form,
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.TEMPLATE,
        'object_name': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.TEMPLATE,
        'template': dashboard_constants.DASHBOARD_TEMPLATES_TEMPLATE_TABLE
    }

    # Get all templates from other users
    other_template_versions = template_version_manager_api.get_all()

    detailed_other_users_templates = []
    for other_template_version in other_template_versions:

        # If the version manager doesn't have a user, the template is global.
        if other_template_version.user is not None:
            detailed_other_users_templates.append({'template_version': other_template_version,
                                                   'template': template_api.get(other_template_version.current),
                                                   'user': user_api.get_user_by_id(other_template_version.user).username,
                                                   'title': other_template_version.title})

    context.update({'other_users_data': detailed_other_users_templates,
                    'number_columns': 4, 'menu': True})

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

    _handle_asset_modals(assets,
                         modals,
                         delete=False,
                         change_owner=False,
                         menu=True)

    return admin_render(request, dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
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

    # Add user_form for change owner
    user_form = UserForm(request.user)
    context = {
        'user_form': user_form,
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.TYPE,
        'object_name': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.TYPE,
        'template': dashboard_constants.DASHBOARD_TYPES_TEMPLATE_TABLE
    }

    # Get all types from other users
    other_type_versions = type_version_manager_api.get_all_version_manager()

    detailed_other_users_types = []
    for other_type_version in other_type_versions:

        # If the version manager doesn't have a user, the type is global.
        if other_type_version.user is not None:
            detailed_other_users_types.append({'type_version': other_type_version,
                                               'type': type_api.get(other_type_version.current),
                                               'user': user_api.get_user_by_id(other_type_version.user).username,
                                               'title': other_type_version.title})

        context.update({'other_users_data': detailed_other_users_types,
                        'number_columns': 4,
                        'action_form': ActionForm([('1', 'Delete selected types')]),
                        'menu': True})

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

    _handle_asset_modals(assets,
                         modals,
                         delete=False,
                         change_owner=False,
                         menu=True)

    return admin_render(request, dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
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

    context = {
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FILE,
        'template': dashboard_constants.DASHBOARD_FILES_TEMPLATE_TABLE
    }

    # Get all files from other users
    other_files = blob_api.get_all()

    detailed_other_users_files = []
    for other_file in other_files:
        detailed_other_users_files.append({'user': user_api.get_user_by_id(other_file.user_id).username,
                                           'date': other_file.id.generation_time,
                                           'file': other_file,
                                           'url': blob_utils.get_blob_download_uri(other_file, request)
                                           })

    context.update({'other_users_data': detailed_other_users_files,
                    'number_columns': 5,
                    'action_form': ActionForm([('1', 'Delete selected files')]),
                    'menu': True
                    })

    modals = []

    assets = {
        "css": copy.deepcopy(dashboard_constants.CSS_COMMON),

        "js": []
    }

    _handle_asset_modals(assets,
                         modals,
                         delete=True,
                         change_owner=False,
                         menu=True)

    return admin_render(request, dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
                        context=context,
                        assets=assets,
                        modals=modals)


@login_required(login_url=reverse_lazy("core_main_app_login"))
def dashboard_workspaces(request):
    """ List the workspaces.

    Args:
        request:
    Return:
    """

    user_workspaces = workspace_api.get_all()
    detailed_user_workspaces = []
    for user_workspace in user_workspaces:
        detailed_user_workspaces.append({'user': user_api.get_user_by_id(user_workspace.owner).username,
                                         'is_owner': True,
                                         'name': user_workspace.title,
                                         'workspace': user_workspace,
                                         'can_read': True,
                                         'can_write': True,
                                         'is_public': workspace_api.is_workspace_public(user_workspace)
                                         })

    context = {
        'workspace_form': WorkspaceForm(),
        'other_users_data': detailed_user_workspaces,
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.WORKSPACE,
        'template': dashboard_constants.DASHBOARD_WORKSPACES_TEMPLATE_TABLE,
        'number_columns': 5,
        'create_workspace': False
    }

    modals = ["core_main_app/user/workspaces/list/create_workspace.html",
              "core_main_app/user/workspaces/list/modals/set_public.html"]

    assets = {
        "css": copy.deepcopy(dashboard_constants.CSS_COMMON),

        "js": [{
                    "path": 'core_main_app/user/js/workspaces/list/modals/set_public.js',
                    "is_raw": False
               }]
    }

    _handle_asset_modals(assets,
                         modals,
                         delete=True,
                         change_owner=False,
                         menu=False)

    return admin_render(request,
                        dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
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

    assets['js'].append({
                            "path": dashboard_constants.JS_INIT_ADMIN,
                            "is_raw": True
                        })
    assets['js'].append({
                            "path": dashboard_constants.JS_ADMIN_ACTION_DASHBOARD,
                            "is_raw": True
                        })
    assets['js'].append({
                            "path": dashboard_constants.JS_ADMIN_TABLE,
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
                            "path": dashboard_constants.JS_ADMIN_COUNT_CHECK,
                            "is_raw": True
                        })
    assets['js'].append({
                            "path": dashboard_constants.JS_ADMIN_RESET_CHECKBOX,
                            "is_raw": True
                        })
    assets['js'].append({
                            "path": dashboard_constants.JS_ADMIN_SELECT_ALL,
                            "is_raw": True
                        })
    assets['js'].append({
                            "path": dashboard_constants.JS_ADMIN_SELETED_ELEMENT,
                            "is_raw": False
                        })
    assets['js'].append({
                            "path": dashboard_constants.JS_ADMIN_INIT_MENU,
                            "is_raw": False
                        })
