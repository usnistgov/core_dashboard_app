"""
    Views available for the user
"""

import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from password_policies.views import PasswordChangeFormView

import core_curate_app.components.curate_data_structure.api as curate_data_structure_api
import core_main_app.components.version_manager.api as version_manager_api
from core_dashboard_app import constants as dashboard_constants
from core_dashboard_app.views.forms import ActionForm, UserForm
from core_main_app.components.data import api as data_api
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.user import api as user_api
from core_main_app.utils.datetime_tools.date_time_encoder import DateTimeEncoder
from core_main_app.utils.rendering import render
from core_main_app.views.admin.forms import EditProfileForm


@login_required(login_url=reverse_lazy("core_main_app_login"))
def home(request):
    """ Home page.

    Args:
        request:

    Returns:
    """
    return render(request, dashboard_constants.DASHBOARD_HOME_TEMPLATE)


@login_required(login_url=reverse_lazy("core_main_app_login"))
def my_profile(request):
    """ User's profile information page.

    Args:
        request:

    Returns:
    """
    return render(request, dashboard_constants.DASHBOARD_PROFILE_TEMPLATE)


@login_required(login_url=reverse_lazy("core_main_app_login"))
def my_profile_edit(request):
    """ Edit the profile.

    Args:
        request:

    Returns:
    """
    assets = {
        "css": ["core_dashboard_app/css/exploreTabs.css"]
    }

    if request.method == 'POST':
        form = _get_edit_profile_form(request=request, url=dashboard_constants.DASHBOARD_PROFILE_EDIT_TEMPLATE)
        if form.is_valid():
            user = request.user
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.email = request.POST['email']
            try:
                user_api.upsert(user)
            except IntegrityError as e:
                if 'unique constraint' in e.message:
                    message = "A user with the same username already exists."
                    return render(request, dashboard_constants.DASHBOARD_PROFILE_EDIT_TEMPLATE,
                                  context={'form': form, 'action_result': message}, assets=assets)
                else:
                    _error_while_saving(request, form, assets)
            except Exception, e:
                _error_while_saving(request, form, assets)

            messages.add_message(request, messages.INFO, 'Profile information edited with success.')
            return HttpResponseRedirect(reverse("core_dashboard_profile"))
    else:
        user = request.user
        data = {'firstname': user.first_name,
                'lastname': user.last_name,
                'username': user.username,
                'email': user.email}
        form = _get_edit_profile_form(request, dashboard_constants.DASHBOARD_PROFILE_TEMPLATE, data)

    return render(request, dashboard_constants.DASHBOARD_PROFILE_EDIT_TEMPLATE, context={'form': form}, assets=assets)


def _get_edit_profile_form(request, url, data=None):
    """ Edit the profile.

    Args:
        request
        url
        data

    Returns:
    """
    data = request.POST if data is None else data
    try:
        return EditProfileForm(data)
    except Exception as e:
        message = "A problem with the form has occurred."
        return render(request, url,
                      context={'action_result': message})


def _error_while_saving(request, form, assets):
    """ Raise exception if uncatched problems occurred while saving.

    Args:
        request
        form

    Returns:
    """
    message = "A problem has occurred while saving the user."
    return render(request, dashboard_constants.DASHBOARD_PROFILE_EDIT_TEMPLATE,
                  context={'form': form, 'action_result': message}, assets=assets)


class UserDashboardPasswordChangeFormView(PasswordChangeFormView):

    def get(self, request, *args, **kwargs):
        """

        Args: request:
        Args: args:
        Args: kwargs:
        Returns:
        """
        assets = {
            "css": ["core_dashboard_app/css/exploreTabs.css"]
        }
        return render(request, self.template_name, context={'form': self.get_form()}, assets=assets)

    def form_valid(self, form):
        """

        Args: form
        Returns:
        """
        messages.success(self.request, "Password changed with success.")
        return super(UserDashboardPasswordChangeFormView, self).form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.

        Args: form
        Returns:
        """
        assets = {
            "css": ["core_dashboard_app/css/exploreTabs.css"]
        }
        return render(None, self.template_name, context={'form': form}, assets=assets)

    def get_success_url(self):
        """
        Returns a query string field with a previous URL if available (Mimicing
        the login view. Used on forced password changes, to know which URL the
        user was requesting before the password change.)
        If not returns the :attr:`~PasswordChangeFormView.success_url` attribute
        if set, otherwise the URL to the :class:`PasswordChangeDoneView`.
        """
        checked = '_password_policies_last_checked'
        last = '_password_policies_last_changed'
        required = '_password_policies_change_required'
        now = json.dumps(timezone.now(), cls=DateTimeEncoder)
        self.request.session[checked] = now
        self.request.session[last] = now
        self.request.session[required] = False
        redirect_to = self.request.POST.get(self.redirect_field_name, '')
        if redirect_to:
            url = redirect_to
        elif self.success_url:
            url = self.success_url
        else:
            url = reverse('password_change_done')
        return url


@login_required(login_url=reverse_lazy("core_main_app_login"))
def dashboard_records(request):
    """ List the records.

    Args:
        request:
    Return:
    """

    # Get user records
    user_data = sorted(data_api.get_all_by_user_id(request.user.id),
                       key=lambda data: data['last_modification_date'], reverse=True)

    # Add user_form for change owner
    user_form = UserForm(request.user)
    context = {
        'user_data': user_data,
        'user_form': user_form,
        'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.RECORD
    }

    # If the user is an admin, we get records for other users
    if request.user.is_staff:

        # Get all username and corresponding ids
        user_names = dict((str(x.id), x.username) for x in user_api.get_all_users())

        # Get all records from other users
        other_users_data = sorted(data_api.get_all_except_user_id(request.user.id),
                                  key=lambda data: data['last_modification_date'], reverse=True)

        context.update({'other_user_data': other_users_data,
                        'usernames': user_names,
                        'action_form': ActionForm([('1', 'Delete selected records'),
                                                   ('2', 'Change owner of selected records')])})

    modals = []

    assets = {
        "css": dashboard_constants.CSS_COMMON,

        "js": []
    }

    _handle_asset_modals(request.user.is_staff, assets, modals, dashboard_constants.JS_RECORD, True, True)

    return render(request, dashboard_constants.DASHBOARD_RECORDS_TEMPLATE,
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

    context = {'forms': detailed_forms,
               'user_form': user_form,
               'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FORM
               }

    # If the user is an admin, we get records for other users
    if request.user.is_staff:

        # Get all username and corresponding ids
        user_names = dict((str(x.id), x.username) for x in user_api.get_all_users())

        # Get all forms from other users
        other_user_forms = curate_data_structure_api.get_all_except_user_id_with_no_data(request.user.id)

        other_detailed_forms = []
        for form in other_user_forms:
            template_name = version_manager_api.get_from_version(form.template).title
            other_detailed_forms.append({'form': form,
                                         'template': template_name})

        context.update({'other_user_forms': other_detailed_forms,
                        'usernames': user_names,
                        'action_form': ActionForm(
                            [('1', 'Delete selected forms'), ('2', 'Change owner of selected forms')])})

    modals = []

    assets = {
        "css": dashboard_constants.CSS_COMMON,

        "js": []
    }

    _handle_asset_modals(request.user.is_staff, assets, modals, dashboard_constants.JS_FORM, True, True)

    return render(request, dashboard_constants.DASHBOARD_FORMS_TEMPLATE,
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
        'object_name': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.TEMPLATE
    }
    # If the user is an admin, we get records for other users
    if request.user.is_staff:

        # Get all templates from other users
        other_template_versions = template_version_manager_api.get_all_version_manager_except_user_id(request.user.id)

        detailed_other_users_templates = []
        for other_template_version in other_template_versions:

            # If the version manager doesn't have a user, the template is global.
            if other_template_version.user is not None:
                detailed_other_users_templates.append({'template_version': other_template_version,
                                                       'template': template_api.get(other_template_version.current),
                                                       'user': user_api.get_user_by_id(other_template_version.user).username,
                                                       'title': other_template_version.title})

        context.update({'other_users_data': detailed_other_users_templates})

    modals = [
                "core_main_app/admin/templates/list/modals/edit.html",
                "core_main_app/admin/templates/list/modals/disable.html"
            ]

    assets = {
        "css": dashboard_constants.CSS_COMMON,

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

    _handle_asset_modals(request.user.is_staff, assets, modals,
                         dashboard_constants.JS_TEMPLATE_TYPE,
                         delete=False,
                         change_owner=False)

    return render(request, dashboard_constants.DASHBOARD_TEMPLATES_AND_TYPES_TEMPLATE,
                  context=context,
                  assets=assets,
                  modals=modals)


def _handle_asset_modals(user_is_staff, assets, modal, functional_asset, delete=False, change_owner=False):
    """ Add needed assets.

    Args:
        user_is_staff
        assets
        modal
        functional_asset
        delete
        change_owner

    Return:
    """

    # Admin or user assets
    assets['js'].extend(dashboard_constants.JS_ADMIN if user_is_staff else dashboard_constants.JS_USER)

    # Common asset
    assets['js'].extend(dashboard_constants.JS_COMMON)
    if delete:
        assets['js'].extend(dashboard_constants.JS_COMMON_FUNCTION_DELETE)
        modal.extend(dashboard_constants.MODALS_COMMON_DELETE)
    if change_owner:
        assets['js'].extend(dashboard_constants.JS_COMMON_FUNCTION_CHANGE_OWNER)
        modal.extend(dashboard_constants.MODALS_COMMON_CHANGE_OWNER)

    # Functional asset
    assets['js'].extend(functional_asset)
