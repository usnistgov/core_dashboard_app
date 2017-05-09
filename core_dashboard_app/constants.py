from core_dashboard_app.enum import enum


# Templates
DASHBOARD_HOME_TEMPLATE = 'core_dashboard_app/home.html'
DASHBOARD_PROFILE_TEMPLATE = 'core_dashboard_app/my_profile.html'
DASHBOARD_PROFILE_EDIT_TEMPLATE = 'core_dashboard_app/my_profile_edit.html'
DASHBOARD_RECORDS_TEMPLATE = 'core_dashboard_app/my_dashboard_my_records.html'
DASHBOARD_FORMS_TEMPLATE = 'core_dashboard_app/my_dashboard_my_forms.html'


FUNCTIONAL_OBJECT_ENUM = enum(RECORD='record',
                              FORM='form')
