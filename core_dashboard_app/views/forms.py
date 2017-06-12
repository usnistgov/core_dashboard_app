from django import forms
from core_main_app.components.user.api import get_all_users


class ActionForm(forms.Form):
    """
    Form to select the action in the user dashboard.
    """
    actions = forms.ChoiceField(label='', required=True, choices=[])

    def __init__(self, list_actions):
        super(ActionForm, self).__init__()
        self.fields['actions'].choices = list_actions


class UserForm(forms.Form):
    """
    Form to select a user.
    """
    users = forms.ChoiceField(label='', required=True)
    USERS_OPTIONS = []

    def __init__(self, currentUser):
        self.USERS_OPTIONS = []
        self.USERS_OPTIONS.append(('', '-----------'))

        # We retrieve all users
        sort_users = get_all_users()
        # We sort by username, case insensitive
        sort_users = sorted(sort_users, key=lambda s: s.username.lower())

        # We add them
        for user in sort_users:
            if user.id != currentUser.id:
                self.USERS_OPTIONS.append((user.id, user.username))

        super(UserForm, self).__init__()
        self.fields['users'].choices = []
        self.fields['users'].choices = self.USERS_OPTIONS
