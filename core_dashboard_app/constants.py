"""
    User Dashboard constants
"""
from core_dashboard_app.enum import enum


# Templates
DASHBOARD_HOME_TEMPLATE = 'core_dashboard_app/home.html'
DASHBOARD_PROFILE_TEMPLATE = 'core_dashboard_app/my_profile.html'
DASHBOARD_PROFILE_EDIT_TEMPLATE = 'core_dashboard_app/my_profile_edit.html'
DASHBOARD_TEMPLATE = 'core_dashboard_app/my_dashboard.html'
ADMIN_DASHBOARD_TEMPLATE = 'core_dashboard_app/admin/dashboard.html'

# Tables
DASHBOARD_RECORDS_TEMPLATE_TABLE = 'core_dashboard_app/list/my_dashboard_my_records_table.html'
DASHBOARD_RECORDS_TEMPLATE_TABLE_DATATABLE = 'core_dashboard_app/list/my_dashboard_my_records_table_datatable.html'
DASHBOARD_RECORDS_TEMPLATE_TABLE_PAGINATION = 'core_dashboard_app/list/my_dashboard_my_records_table_pagination.html'
DASHBOARD_FORMS_TEMPLATE_TABLE = 'core_dashboard_app/list/my_dashboard_my_forms_table.html'
DASHBOARD_TEMPLATES_TEMPLATE_TABLE = 'core_dashboard_app/list/my_dashboard_my_templates_table.html'
DASHBOARD_TYPES_TEMPLATE_TABLE = 'core_dashboard_app/list/my_dashboard_my_types_table.html'
DASHBOARD_FILES_TEMPLATE_TABLE='core_dashboard_app/list/my_dashboard_my_files_table.html'
DASHBOARD_WORKSPACES_TEMPLATE_TABLE='core_dashboard_app/list/my_dashboard_my_workspaces_table.html'

# Assets
MODALS_COMMON_DELETE = "core_dashboard_app/list/modals/delete_document.html"
MODALS_COMMON_CHANGE_OWNER = "core_dashboard_app/list/modals/change_owner.html"

# TODO: replace with the constants in core main app once they are done
CSS_COMMON = [
                'core_main_app/common/css/XMLTree.css',
                'core_main_app/libs/datatables/1.10.13/css/jquery.dataTables.css'
             ]
JS_COMMON = [{
                "path": 'core_main_app/libs/datatables/1.10.13/js/jquery.dataTables.js',
                "is_raw": True
            },
            {
                "path": 'core_dashboard_app/user/js/init.js',
                "is_raw": False
            }]

JS_INIT_USER = 'core_dashboard_app/user/js/init_user.js'
JS_USER_TABLE = 'core_dashboard_app/user/js/user_table.js'
JS_USER_SELECTED_ELEMENT = 'core_dashboard_app/user/js/get_selected_document.js'
JS_COMMON_FUNCTION_DELETE = 'core_dashboard_app/user/js/list/modals/delete_document.js'
JS_COMMON_FUNCTION_CHANGE_OWNER = 'core_dashboard_app/user/js/list/modals/change_owner.js'
JS_EDIT_RECORD = 'core_dashboard_app/user/js/list/edit_record.js'
USER_VIEW_RECORD_RAW = 'core_dashboard_app/user/js/list/view_record.raw.js'
JS_VIEW_RECORD = 'core_dashboard_app/common/js/list/view_record.js'

# Admin
JS_ADMIN_COUNT_CHECK = 'core_dashboard_app/admin/js/count_checked.js'
JS_ADMIN_RESET_CHECKBOX = 'core_dashboard_app/admin/js/reset_checkbox.js'
JS_ADMIN_SELECT_ALL = 'core_dashboard_app/admin/js/select_all.js'
JS_ADMIN_SELETED_ELEMENT = 'core_dashboard_app/admin/js/get_selected_document_admin.js'
JS_ADMIN_INIT_MENU = 'core_dashboard_app/admin/js/init_admin_menu.js'
JS_INIT_ADMIN = 'core_dashboard_app/admin/js/init_admin.js'
JS_ADMIN_ACTION_DASHBOARD = 'core_dashboard_app/admin/js/action_dashboard.js'
JS_ADMIN_TABLE = 'core_dashboard_app/admin/js/admin_table.js'
ADMIN_VIEW_RECORD_RAW = 'core_dashboard_app/admin/js/list/view_record.raw.js'


FUNCTIONAL_OBJECT_ENUM = enum(RECORD='record',
                              FORM='form',
                              TEMPLATE='template',
                              TYPE='type',
                              FILE='file',
                              WORKSPACE='workspace')
