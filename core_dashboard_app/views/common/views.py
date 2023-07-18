""" User Views
"""
import copy

from core_main_app.components.workspace.api import (
    check_if_workspace_can_be_changed,
)

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from core_dashboard_common_app import constants as dashboard_constants
from core_dashboard_common_app.views.common.forms import UserForm
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.blob import api as workspace_blob_api
from core_main_app.components.blob import utils as blob_utils
from core_main_app.components.data import api as workspace_data_api
from core_main_app.components.user import api as user_api
from core_main_app.components.workspace import api as workspace_api
from django.conf import settings
from core_main_app.utils.pagination.django_paginator.results_paginator import (
    ResultsPaginator,
)
from core_main_app.views.common.views import CommonView

if "core_curate_app" in settings.INSTALLED_APPS:
    import core_curate_app.components.curate_data_structure.api as curate_data_structure_api


class DashboardWorkspaceTabs(CommonView):
    """Workspace Tab Page"""

    template = "core_dashboard_app/user/my_dashboard_container.html"
    data_template = "core_dashboard_app/common/list/my_dashboard_tabs.html"

    def get(self, request, workspace_id):
        """get workspace page

        Args:
            request:
            workspace_id:

        Returns:

        """
        # Initialize necessary variables
        user_can_read = False

        tab_selected = request.GET.get("tab", "data")
        data_count = 0
        files_count = 0
        context = {}

        try:
            workspace = workspace_api.get_by_id(workspace_id)
        except exceptions.DoesNotExist:
            error_message = "Workspace not found"
            status_code = 404
            return self._show_error(request, error_message, status_code)

        try:
            user_can_read = workspace_api.can_user_read_workspace(
                workspace, request.user
            )
            if not user_can_read:
                error_message = "Access Forbidden"
                status_code = 403
                return self._show_error(request, error_message, status_code)

            # Figure out the items to render on the page
            items_to_render = []
            data = workspace_data_api.get_all_by_workspace(
                workspace, request.user
            )
            data_count = data.count()
            files = workspace_blob_api.get_all_by_workspace(
                workspace, request.user
            )
            files_count = files.count()

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
                    {
                        "document": dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FILE.value
                    }
                )
        except AccessControlError:
            items_to_render = workspace_data_api.get_none()

        user_can_write = workspace_api.can_user_write_workspace(
            workspace, request.user
        )

        # Paginator
        page = request.GET.get("page", 1)
        results_paginator = ResultsPaginator.get_results(
            items_to_render,
            page,
            settings.RECORD_PER_PAGE_PAGINATION,
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
                "number_total_data": data_count,
                "number_total_files": files_count,
                "share_pid_button": "core_linked_records_app"
                in settings.INSTALLED_APPS,
            }
        )

        if self.administration and workspace.owner:
            context.update(
                {
                    "owner": user_api.get_user_by_id(workspace.owner).username,
                    "owner_change_url": reverse(
                        "admin:auth_user_change", args=[workspace.owner]
                    ),
                }
            )

        # Get all username and corresponding ids
        user_names = dict(
            (str(x.id), x.username) for x in user_api.get_all_users()
        )
        context.update({"usernames": user_names})

        modals = [
            dashboard_constants.MODALS_COMMON_CHANGE_OWNER,
            dashboard_constants.MODALS_COMMON_DELETE,
            "core_main_app/user/workspaces/list/modals/assign_workspace.html",
        ]

        assets = self._get_assets()

        if "core_file_preview_app" in settings.INSTALLED_APPS:
            assets["js"].extend(
                [
                    {
                        "path": "core_file_preview_app/user/js/file_preview.js",
                        "is_raw": False,
                    }
                ]
            )
            assets["css"].append(
                "core_file_preview_app/user/css/file_preview.css"
            )
            modals.append("core_file_preview_app/user/file_preview_modal.html")

        if context["share_pid_button"]:
            modals.append(
                "core_linked_records_app/user/sharing/data_detail/modal.html"
            )
            assets["css"].append("core_main_app/common/css/share_link.css"),

            assets["js"] += [
                {
                    "path": "core_main_app/user/js/sharing_modal.js",
                    "is_raw": False,
                },
                {
                    "path": "core_linked_records_app/user/js/sharing/common_list.js",
                    "is_raw": False,
                },
                {
                    "path": "core_linked_records_app/user/js/sharing/data_list.js",
                    "is_raw": False,
                },
            ]

        # Set page title
        context.update({"page_title": "Dashboard"})
        return self.common_render(
            request,
            self.template,
            context=context,
            assets=assets,
            modals=modals,
        )

    def _format_document_context(
        self,
        request,
        document_list,
        user_can_read,
        user_can_write,
        tab_selected,
    ):
        detailed_documents = []
        user = request.user
        for document in document_list:
            is_owner = (
                str(document.user_id) == str(user.id) or self.administration
            )
            document_context = {
                "can_read": user_can_read or is_owner,
                "can_write": user_can_write or is_owner,
                "can_change_workspace": check_if_workspace_can_be_changed(
                    document
                ),
                "is_owner": is_owner,
            }
            if tab_selected == "data":
                forms_count = (
                    len(
                        curate_data_structure_api.get_all_curate_data_structures_by_data(
                            document, user
                        )
                    )
                    if self.administration
                    else 0
                )
                document_context.update(
                    {
                        "data": document,
                        "form_id": self._get_form(document, user),
                        "forms_count": forms_count,
                    }
                )
            elif tab_selected == "file":
                try:
                    username = user_api.get_user_by_id(
                        document.user_id
                    ).username
                except ObjectDoesNotExist:
                    username = "None"
                document_context.update(
                    {
                        "file": document,
                        "url": f"{reverse('core_main_app_blob_detail')}?id={document.id}",
                        "download_url": blob_utils.get_blob_download_uri(
                            document, request
                        ),
                        "user": username,
                        "date": document.creation_date,
                    }
                )
            detailed_documents.append(document_context)
        return detailed_documents

    def _get_form(self, data, user):
        try:
            return curate_data_structure_api.get_by_data_id_and_user(
                data.id, user
            ).id
        except DoesNotExist:
            return None

    def _get_assets(self):
        assets = {
            "css": copy.deepcopy(dashboard_constants.CSS_COMMON),
            "js": [
                {
                    "path": "core_main_app/user/js/workspaces/list/modals/assign_workspace.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/user/js/workspaces/list/modals/assign_data_workspace.raw.js",
                    "is_raw": True,
                },
                {
                    "path": dashboard_constants.USER_VIEW_RECORD_RAW,
                    "is_raw": True,
                },
                {"path": dashboard_constants.JS_EDIT_RECORD, "is_raw": False},
                {
                    "path": dashboard_constants.JS_USER_SELECTED_ELEMENT,
                    "is_raw": False,
                },
                {
                    "path": dashboard_constants.JS_OPEN_DOCUMENT,
                    "is_raw": False,
                },
                {
                    "path": "core_dashboard_common_app/common/js/list/open_record.raw.js",
                    "is_raw": True,
                },
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
                {
                    "path": "core_dashboard_common_app/common/js/list/delete_data_draft.js",
                    "is_raw": False,
                },
            ],
        }

        assets["css"].append(
            "core_dashboard_app/common/css/my_dashboard_tabs.css"
        )

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

    def _show_error(self, request, error_message, status_code):
        return self.common_render(
            request,
            "core_main_app/common/commons/error.html",
            context={
                "error": f"Unable to access the requested workspace: {error_message}.",
                "status_code": status_code,
                "page_title": "Error",
            },
            assets={
                "js": [
                    {
                        "path": "core_main_app/common/js/backtoprevious.js",
                        "is_raw": True,
                    }
                ]
            },
        )
