"""
    Views available for the user
"""

# from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.db import IntegrityError
from django.utils import timezone
from password_policies.views import PasswordChangeFormView
import json

from core_dashboard_app import settings
from core_main_app.utils.rendering import render
from core_main_app.views.admin.forms import EditProfileForm
from core_main_app.components.user import api as user_api
from core_main_app.utils.datetime_tools.date_time_encoder import DateTimeEncoder


# FIXME: put it back when we will be able to log in
# @login_required(login_url='/login')
def home(request):
    """

    :args request:
    :return:
    """
    # FIXME: find a solution to finder
    # if finders.find(DASHBOARD_HOME_TEMPLATE) is None:
    #     raise exceptions.DoesNotExist()
    return render(request, settings.DASHBOARD_HOME_TEMPLATE)


# FIXME: put it back when we will be able to log in
# @login_required(login_url='/login')
def my_profile(request):
    """
    User's profile information page
    :args request:
    :return:
    """
    return render(request, settings.DASHBOARD_PROFILE_TEMPLATE)


# FIXME: put it back when we will be able to log in
# @login_required(login_url='/login')
def my_profile_edit(request):
    """

    :args request:
    :return:
    """
    assets = {
        "css": ["core_dashboard_app/css/exploreTabs.css"]
    }

    if request.method == 'POST':
        form = get_edit_profile_form(request=request, url=settings.DASHBOARD_PROFILE_EDIT_TEMPLATE)
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
                    return render(request, settings.DASHBOARD_PROFILE_EDIT_TEMPLATE,
                                  context={'form': form, 'action_result': message}, assets=assets)
                else:
                    error_while_saving(request, form, assets)
            except Exception, e:
                error_while_saving(request, form, assets)

            messages.add_message(request, messages.INFO, 'Profile information edited with success.')
            return HttpResponseRedirect(reverse("core_dashboard_profile"))
    else:
        user = request.user
        data = {'firstname': user.first_name,
                'lastname': user.last_name,
                'username': user.username,
                'email': user.email}
        form = get_edit_profile_form(request, settings.DASHBOARD_PROFILE_TEMPLATE, data)

    return render(request, settings.DASHBOARD_PROFILE_EDIT_TEMPLATE, context={'form': form}, assets=assets)


def get_edit_profile_form(request, url, data=None):
    """

    :args request:
    :args url:
    :args data:
    :return:
    """
    data = request.POST if data is None else data
    try:
        return EditProfileForm(data)
    except Exception as e:
        message = "A problem with the form has occurred."
        return render(request, url,
                      context={'action_result': message})


def error_while_saving(request, form, assets):
    """
    Raise exception if uncatched problems occurred while saving
    :args request:
    :args form:
    :return:
    """
    message = "A problem has occurred while saving the user."
    return render(request, settings.DASHBOARD_PROFILE_EDIT_TEMPLATE,
                  context={'form': form, 'action_result': message}, assets=assets)


class UserDashboardPasswordChangeFormView(PasswordChangeFormView):

    def get(self, request, *args, **kwargs):
        """

        :args request:
        :args args:
        :args kwargs:
        :return:
        """
        assets = {
            "css": ["core_dashboard_app/css/exploreTabs.css"]
        }
        return render(request, self.template_name, context={'form': self.get_form()}, assets=assets)

    def form_valid(self, form):
        """

        :args form:
        :return:
        """
        messages.success(self.request, "Password changed with success.")
        return super(UserDashboardPasswordChangeFormView, self).form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
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
