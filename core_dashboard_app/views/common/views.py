"""
    Common views
"""
import copy
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from password_policies.views import PasswordChangeFormView

from core_dashboard_app import constants as dashboard_constants
from core_dashboard_app import settings
from core_dashboard_app.views.common.forms import ActionForm, UserForm
from core_main_app.components.blob import api as blob_api, utils as blob_utils
from core_main_app.components.data import api as data_api
from core_main_app.components.user import api as user_api
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.datetime_tools.date_time_encoder import DateTimeEncoder
from core_main_app.utils.pagination.django_paginator.results_paginator import ResultsPaginator
from core_main_app.utils.rendering import render
from core_main_app.views.admin.forms import EditProfileForm
from core_main_app.views.common.views import CommonView
from core_main_app.components.blob import api as blob_api, utils as blob_utils
from core_main_app.settings import INSTALLED_APPS
if 'core_curate_app' in INSTALLED_APPS:
    import core_curate_app.components.curate_data_structure.api as curate_data_structure_api


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
                                  context={'form': form, 'action_result': message})
                else:
                    _error_while_saving(request, form)
            except Exception, e:
                _error_while_saving(request, form)

            messages.add_message(request, messages.INFO, 'Profile information edited with success.')
            return HttpResponseRedirect(reverse("core_dashboard_profile"))
    else:
        user = request.user
        data = {'firstname': user.first_name,
                'lastname': user.last_name,
                'username': user.username,
                'email': user.email}
        form = _get_edit_profile_form(request, dashboard_constants.DASHBOARD_PROFILE_TEMPLATE, data)

    return render(request, dashboard_constants.DASHBOARD_PROFILE_EDIT_TEMPLATE, context={'form': form})


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


def _error_while_saving(request, form):
    """ Raise exception if uncatched problems occurred while saving.

    Args:
        request
        form

    Returns:
    """
    message = "A problem has occurred while saving the user."
    return render(request, dashboard_constants.DASHBOARD_PROFILE_EDIT_TEMPLATE,
                  context={'form': form, 'action_result': message})


class UserDashboardPasswordChangeFormView(PasswordChangeFormView):

    def get(self, request, *args, **kwargs):
        """

        Args: request:
        Args: args:
        Args: kwargs:
        Returns:
        """
        return render(request, self.template_name, context={'form': self.get_form()})

    def get_form(self):
        """ Return the form.

        Returns: The form.
        """

        return super(UserDashboardPasswordChangeFormView, self).get_form(self.form_class)

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
        return render(self.request, self.template_name, context={'form': form})

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


class DashboardRecords(CommonView):
    """ List the records.
    """

    template = dashboard_constants.DASHBOARD_TEMPLATE

    def get(self, request, *args, **kwargs):

        # Get records
        if self.administration:
            try:
                loaded_data = data_api.get_all(request.user, '-last_modification_date')
            except AccessControlError, ace:
                loaded_data = []
            # Get all username and corresponding ids
            user_names = dict((str(x.id), x.username) for x in user_api.get_all_users())
        else:
            loaded_data = data_api.get_all_by_user(request.user, '-last_modification_date')

        # Paginator
        page = request.GET.get('page', 1)
        results_paginator = ResultsPaginator.get_results(loaded_data, page, settings.RECORD_PER_PAGE_PAGINATION)

        detailed_loaded_data = []
        for data in results_paginator.object_list:
            detailed_loaded_data.append({'data': data,
                                         'can_read': True,
                                         'can_write': True,
                                         'is_owner': True})

        results_paginator.object_list = detailed_loaded_data

        # Add user_form for change owner
        user_form = UserForm(request.user)
        context = {
            'other_users_data': results_paginator,
            'user_form': user_form,
            'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.RECORD,
            'template': dashboard_constants.DASHBOARD_RECORDS_TEMPLATE_TABLE_PAGINATION,
            'action_form': ActionForm([('1', 'Delete selected records'),
                                       ('2', 'Change owner of selected records')]),
            'menu': self.administration,
            'administration': self.administration
        }

        if self.administration:
            context.update({'usernames': user_names})

        modals = ["core_main_app/user/workspaces/list/modals/assign_workspace.html",
                  dashboard_constants.MODALS_COMMON_DELETE,
                  dashboard_constants.MODALS_COMMON_CHANGE_OWNER
                  ]

        assets = {
            "css": copy.deepcopy(dashboard_constants.CSS_COMMON),

            "js": [
                    {
                        "path": 'core_main_app/user/js/workspaces/list/modals/assign_workspace.js',
                        "is_raw": False
                    },
                    {
                        "path": 'core_dashboard_app/common/js/init_pagination.js',
                        "is_raw": False
                    },
                    {
                        "path": 'core_dashboard_app/user/js/init.raw.js',
                        "is_raw": True
                    },
                    {
                        "path": dashboard_constants.JS_EDIT_RECORD,
                        "is_raw": False
                    },
                    {
                        "path": dashboard_constants.JS_VIEW_RECORD,
                        "is_raw": False
                    },
                    {
                        "path": dashboard_constants.JS_COMMON_FUNCTION_CHANGE_OWNER,
                        "is_raw": False
                    },
                    {
                        "path": dashboard_constants.JS_COMMON_FUNCTION_DELETE,
                        "is_raw": False
                    }
            ]
        }

        # Admin
        if self.administration:
            assets['js'].append({
                                    "path": dashboard_constants.ADMIN_VIEW_RECORD_RAW,
                                    "is_raw": True
                                 })
            assets['js'].append({
                                    "path": 'core_dashboard_app/admin/js/action_dashboard.js',
                                    "is_raw": True
                                })
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
        else:
            assets['js'].append({
                                    "path": dashboard_constants.JS_USER_SELECTED_ELEMENT,
                                    "is_raw": True
                                })
            assets['js'].append({
                                   "path": dashboard_constants.USER_VIEW_RECORD_RAW,
                                   "is_raw": True
                                })

        return self.common_render(request, self.template,
                                  context=context,
                                  assets=assets,
                                  modals=modals)


class DashboardFiles(CommonView):
    """ List the files.
    """

    template = dashboard_constants.DASHBOARD_TEMPLATE

    def get(self, request, *args, **kwargs):
        """ Method GET

        Args:
            request:
            args:
            kwargs:

        Returns:
        """
        if self.administration:
            files = blob_api.get_all()
        else:
            files = blob_api.get_all_by_user_id(request.user.id)

        detailed_file = []
        for file in files:
            detailed_file.append({'user': user_api.get_user_by_id(file.user_id).username,
                                  'date': file.id.generation_time,
                                  'file': file,
                                  'url': blob_utils.get_blob_download_uri(file, request)
                                  })

        context = {
            'user_data': detailed_file,
            'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FILE,
            'template': dashboard_constants.DASHBOARD_FILES_TEMPLATE_TABLE,
            'menu': self.administration,
        }

        if self.administration:
            context.update({'action_form': ActionForm([('1', 'Delete selected files')])
                            })

        modals = [dashboard_constants.MODALS_COMMON_DELETE]

        assets = {
            "css": dashboard_constants.CSS_COMMON,

            "js": [
                    {
                        "path": 'core_dashboard_app/user/js/init.raw.js',
                        "is_raw": True
                    },
                    {
                        "path": dashboard_constants.JS_COMMON_FUNCTION_DELETE,
                        "is_raw": False
                    },
                    {
                        "path": dashboard_constants.JS_USER_SELECTED_ELEMENT,
                        "is_raw": True
                    }
            ]
        }

        # Admin
        if self.administration:
            assets['js'].append({
                "path": 'core_dashboard_app/common/js/init_pagination.js',
                "is_raw": False
            })
            assets['js'].append({
                "path": dashboard_constants.JS_ADMIN_ACTION_DASHBOARD,
                "is_raw": True
            })
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

        return self.common_render(request, self.template,
                                  context=context,
                                  assets=assets,
                                  modals=modals)


class DashboardForms(CommonView):
    """ List the forms.
    """

    template = dashboard_constants.DASHBOARD_TEMPLATE

    def get(self, request, *args, **kwargs):
        """ Method GET

        Args:
            request:
            args:
            kwargs:

        Returns:
        """
        # Get the forms
        if self.administration:
            forms = curate_data_structure_api.get_all_with_no_data()
        else:
            forms = curate_data_structure_api.get_all_by_user_id_with_no_data(request.user.id)

        detailed_forms = []
        for form in forms:
            detailed_forms.append({'form': form})

        context = {'user_data': detailed_forms,
                   'user_form': UserForm(request.user),
                   'document': dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FORM,
                   'template': dashboard_constants.DASHBOARD_FORMS_TEMPLATE_TABLE,
                   'menu': self.administration
                   }

        modals = [dashboard_constants.MODALS_COMMON_DELETE,
                  dashboard_constants.MODALS_COMMON_CHANGE_OWNER
                  ]

        assets = {
            "css": dashboard_constants.CSS_COMMON,

            "js": [{
                        "path": dashboard_constants.JS_COMMON_FUNCTION_DELETE,
                        "is_raw": False
                    },
                    {
                        "path": dashboard_constants.JS_COMMON_FUNCTION_CHANGE_OWNER,
                        "is_raw": False
                    },
                    {
                        "path": 'core_dashboard_app/user/js/init.raw.js',
                        "is_raw": True
                    },
            ]
        }

        if self.administration:
            # Get all username and corresponding ids
            user_names = dict((str(x.id), x.username) for x in user_api.get_all_users())
            context.update({'usernames': user_names,
                            'action_form': ActionForm(
                                [('1', 'Delete selected forms'), ('2', 'Change owner of selected forms')]),
                            })
            assets['js'].append({
                "path": 'core_dashboard_app/common/js/init_pagination.js',
                "is_raw": False
            })
            assets['js'].append({
                "path": dashboard_constants.JS_ADMIN_ACTION_DASHBOARD,
                "is_raw": True
            })
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
        else:
            assets['js'].append({
                "path": dashboard_constants.JS_USER_SELECTED_ELEMENT,
                "is_raw": True
            })

        return self.common_render(request, self.template,
                                  context=context,
                                  assets=assets,
                                  modals=modals)
