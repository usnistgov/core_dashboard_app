from core_dashboard_app.enum import enum


# Templates
DASHBOARD_HOME_TEMPLATE = 'core_dashboard_app/home.html'
DASHBOARD_PROFILE_TEMPLATE = 'core_dashboard_app/my_profile.html'
DASHBOARD_PROFILE_EDIT_TEMPLATE = 'core_dashboard_app/my_profile_edit.html'
DASHBOARD_RECORDS_TEMPLATE = 'core_dashboard_app/my_dashboard_my_records.html'
DASHBOARD_FORMS_TEMPLATE = 'core_dashboard_app/my_dashboard_my_forms.html'
DASHBOARD_TEMPLATES_AND_TYPES_TEMPLATE = 'core_dashboard_app/my_dashboard_my_templates_and_types.html'

# Assets
MODALS_COMMON_DELETE = [
                            "core_dashboard_app/list/modals/delete_document.html"
                       ]

MODALS_COMMON_CHANGE_OWNER = [
                                "core_dashboard_app/list/modals/change_owner.html"
                             ]

CSS_COMMON = [
                'core_main_app/common/css/XMLTree.css',
                'core_main_app/libs/datatables/1.10.13/css/jquery.dataTables.css'
             ]

JS_USER = [{
                "path": 'core_dashboard_app/user/js/init_user.js',
                "is_raw": True
           }]

JS_COMMON = [{
                "path": 'core_main_app/libs/datatables/1.10.13/js/jquery.dataTables.js',
                "is_raw": True
            },
            {
                "path": 'core_dashboard_app/user/js/init.js',
                "is_raw": False
            },
            {
                "path": 'core_dashboard_app/user/js/get_selected_document.js',
                "is_raw": True
            }]

JS_ADMIN = [{
                "path": 'core_dashboard_app/admin/js/count_checked.js',
                "is_raw": True
            },
            {
                "path": 'core_dashboard_app/admin/js/init_admin.js',
                "is_raw": True
            },
            {
                "path": 'core_dashboard_app/admin/js/reset_checkbox.js',
                "is_raw": True
            },
            {
                "path": 'core_dashboard_app/admin/js/select_all.js',
                "is_raw": True
            },
            {
                "path": 'core_dashboard_app/admin/js/action_dashboard.js',
                "is_raw": True
            }]

JS_COMMON_FUNCTION_DELETE = [{
                                "path": 'core_dashboard_app/user/js/list/modals/delete_document.js',
                                "is_raw": False
                             }]

JS_COMMON_FUNCTION_CHANGE_OWNER = [{
                                      "path": 'core_dashboard_app/user/js/list/modals/change_owner.js',
                                      "is_raw": False
                                   }]

JS_RECORD = [{
                "path": 'core_dashboard_app/user/js/records_table.js',
                "is_raw": True
             },
             {
                "path": 'core_dashboard_app/user/js/list/edit_record.js',
                "is_raw": False
             },
             {
                "path": 'core_dashboard_app/user/js/list/view_record.js',
                "is_raw": False
             }]

JS_FORM = [{
                "path": 'core_dashboard_app/user/js/forms_table.js',
                "is_raw": True
           }]

JS_TEMPLATE_TYPE = [{
                        "path": 'core_dashboard_app/user/js/templates_types_table.js',
                        "is_raw": False
                    }]


FUNCTIONAL_OBJECT_ENUM = enum(RECORD='record',
                              FORM='form',
                              TEMPLATE='template')
