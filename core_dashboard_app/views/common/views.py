"""
    Common views
"""
import json

from core_main_app.components.user import api as user_api
from core_main_app.utils.datetime_tools.date_time_encoder import DateTimeEncoder
from core_main_app.utils.rendering import render
from core_main_app.views.admin.forms import EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from password_policies.views import PasswordChangeFormView

from core_dashboard_app import constants as dashboard_constants


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
