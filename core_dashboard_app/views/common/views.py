""" User Views
"""
import copy

from core_dashboard_common_app import constants as dashboard_constants
from core_dashboard_common_app import settings
from core_dashboard_common_app.views.common.forms import UserForm
from core_main_app.components.blob import api as workspace_blob_api
from core_main_app.components.blob import utils as blob_utils
from core_main_app.components.data import api as workspace_data_api
from core_main_app.components.user import api as user_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.settings import INSTALLED_APPS
from core_main_app.utils.pagination.django_paginator.results_paginator import (
    ResultsPaginator,
)
from core_main_app.views.common.views import CommonView
from core_main_app.access_control.exceptions import AccessControlError


class DashboardWorkspaceTabs(CommonView):
    """Workspace Tab Page"""

    template = "core_dashboard_app/user/my_dashboard_container.html"
    data_template = "core_dashboard_app/common/list/my_dashboard_tabs.html"

    def get(self, request, workspace_id, *args, **kwargs):
        workspace = workspace_api.get_by_id(workspace_id)

        # Get the selected tab if given, otherwise data will be selected by default
        tab_selected = request.GET.get("tab", "data")
        items_to_render = []

        context = {}

        try:
            data = workspace_data_api.get_all_by_workspace(workspace, request.user)
            files = workspace_blob_api.get_all_by_workspace(workspace, request.user)

            if tab_selected == "data":
                items_to_render = data
                context.update(
                    {
                        "document": dashboard_constants.FUNCTIONAL_OBJECT_ENUM.RECORD.value
                    }
                )
            elif tab_selected == "file":
                items_to_render = files
                context.update(
                    {"document": dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FILE.value}
                )
        except AccessControlError as ace:
            items_to_render = []

        user_can_read = workspace_api.can_user_read_workspace(workspace, request.user)
        user_can_write = workspace_api.can_user_write_workspace(workspace, request.user)

        # Paginator
        page = request.GET.get("page", 1)
        results_paginator = ResultsPaginator.get_results(
            items_to_render, page, settings.RECORD_PER_PAGE_PAGINATION
        )

        # Data context
        results_paginator.object_list = self._format_document_context(
            request,
            results_paginator.object_list,
            user_can_read,
            user_can_write,
            tab_selected,
        )

        # Add user_form for change owner
        user_form = UserForm(request.user)
        context.update(
            {
                "workspace_id": workspace_id,
                "number_total": items_to_render.count(),
                "user_data": results_paginator,
                "user_form": user_form,
                "template": self.data_template,
                "administration": self.administration,
                "username_list": user_api.get_id_username_dict(
                    user_api.get_all_users()
                ),
                "tab": tab_selected,
                "title": workspace.title,
                "number_total_data": data.count(),
                "number_total_files": files.count(),
            }
        )

        # Get all username and corresponding ids
        user_names = dict((str(x.id), x.username) for x in user_api.get_all_users())
        context.update({"usernames": user_names})

        modals = [
            dashboard_constants.MODALS_COMMON_CHANGE_OWNER,
            dashboard_constants.MODALS_COMMON_DELETE,
        ]

        assets = self._get_assets()

        if "core_file_preview_app" in INSTALLED_APPS:
            assets["js"].extend(
                [
                    {
                        "path": "core_file_preview_app/user/js/file_preview.js",
                        "is_raw": False,
                    }
                ]
            )
            assets["css"].append("core_file_preview_app/user/css/file_preview.css")
            modals.append("core_file_preview_app/user/file_preview_modal.html")

        return self.common_render(
            request, self.template, context=context, assets=assets, modals=modals
        )

    def _format_document_context(
        self, request, document_list, user_can_read, user_can_write, tab_selected
    ):
        detailed_documents = []
        user = request.user
        for document in document_list:
            is_owner = str(document.user_id) == str(user.id) or self.administration
            document_context = {
                "can_read": user_can_read or is_owner,
                "can_write": user_can_write or is_owner,
            }
            if tab_selected == "data":
                document_context.update({"data": document, "is_owner": is_owner})
            elif tab_selected == "file":
                document_context.update(
                    {
                        "file": document,
                        "url": blob_utils.get_blob_download_uri(document, request),
                        "user": user_api.get_user_by_id(document.user_id).username,
                        "date": document.id.generation_time,
                        "is_owner": is_owner,
                    }
                )
            detailed_documents.append(document_context)
        return detailed_documents

    def _get_assets(self):
        assets = {
            "css": copy.deepcopy(dashboard_constants.CSS_COMMON),
            "js": [
                {
                    "path": "core_main_app/user/js/workspaces/list/modals/assign_workspace.js",
                    "is_raw": False,
                },
                {"path": dashboard_constants.USER_VIEW_RECORD_RAW, "is_raw": True},
                {"path": dashboard_constants.JS_EDIT_RECORD, "is_raw": False},
                {"path": dashboard_constants.JS_USER_SELECTED_ELEMENT, "is_raw": False},
                {"path": dashboard_constants.JS_VIEW_RECORD, "is_raw": False},
                {
                    "path": "core_dashboard_common_app/user/js/init.raw.js",
                    "is_raw": True,
                },
                {
                    "path": "core_dashboard_common_app/common/js/init_pagination.js",
                    "is_raw": False,
                },
                {
                    "path": dashboard_constants.JS_COMMON_FUNCTION_CHANGE_OWNER,
                    "is_raw": False,
                },
                {
                    "path": dashboard_constants.JS_COMMON_FUNCTION_DELETE,
                    "is_raw": False,
                },
                {
                    "path": "core_dashboard_app/common/js/my_dashboard_tabs.js",
                    "is_raw": False,
                },
            ],
        }

        assets["css"].append("core_dashboard_app/common/css/my_dashboard_tabs.css")

        if self.administration:
            assets["js"].append(
                {
                    "path": "core_dashboard_app/admin/js/my_dashboard_tabs.raw.js",
                    "is_raw": True,
                }
            )
        else:
            assets["js"].append(
                {
                    "path": "core_dashboard_app/user/js/my_dashboard_tabs.raw.js",
                    "is_raw": True,
                }
            )

        return assets
