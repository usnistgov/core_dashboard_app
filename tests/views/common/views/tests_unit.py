""" Unit tests on common dashboard views.
"""
from unittest import TestCase
from unittest.mock import patch

from core_dashboard_app.views.common import views as common_views
from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.data import api as data_api
from core_main_app.components.blob import api as blob_api
from core_main_app.components.user import api as user_api


class TestDashboardWorkspaceTabsGet(TestCase):
    """Unit tests for the get function DashboardWorkspaceTabs view."""

    @staticmethod
    def mock_render_only_context(
        request, template_name, modals=None, assets=None, context=None
    ):
        """mock_render_only_context"""
        return context

    def setUp(self) -> None:
        """mock_render_only_context"""
        self.workspace_records_view = common_views.DashboardWorkspaceTabs
        self.user = create_mock_user("1", is_superuser=True)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(common_views.DashboardWorkspaceTabs, "_show_error")
    def test_workspace_not_found_renders_error(
        self,
        mock_show_error,
        mock_workspace_get_by_id,
    ):
        """test_workspace_not_found_renders_error"""
        mock_workspace_get_by_id.side_effect = exceptions.DoesNotExist(
            "mock_workspace_get_by_id_exception"
        )
        RequestMock.do_request_get(
            self.workspace_records_view.as_view(),
            self.user,
            param={"workspace_id": 42},
        )
        mock_show_error.assert_called()

    @patch.object(workspace_api, "get_by_id")
    @patch.object(data_api, "get_all_by_workspace")
    @patch.object(blob_api, "get_all_by_workspace")
    @patch.object(workspace_api, "can_user_read_workspace")
    @patch.object(workspace_api, "can_user_write_workspace")
    @patch.object(common_views, "ResultsPaginator")
    @patch.object(common_views, "UserForm")
    @patch.object(user_api, "get_id_username_dict")
    @patch.object(user_api, "get_all_users")
    @patch.object(user_api, "get_user_by_id")
    @patch.object(common_views.DashboardWorkspaceTabs, "common_render")
    def test_user_side_context_has_no_owner_info(
        self,
        mock_common_render,
        mock_get_user_by_id,
        mock_get_all_users,
        mock_get_id_username_dict,
        mock_user_form,
        mock_results_paginator,
        mock_can_user_write_workspace,
        mock_can_user_read_workspace,
        mock_get_all_blob_by_workspace,
        mock_get_all_data_by_workspace,
        mock_workspace_get_by_id,
    ):
        """test_user_side_context_has_no_owner_info"""
        mock_common_render.side_effect = self.mock_render_only_context

        self.workspace_records_view.administration = False
        response = RequestMock.do_request_get(
            self.workspace_records_view.as_view(),
            self.user,
            param={"workspace_id": 42},
        )

        self.assertNotIn("owner", response.keys())
        self.assertNotIn("owner_change_url", response.keys())

    @patch.object(workspace_api, "get_by_id")
    @patch.object(data_api, "get_all_by_workspace")
    @patch.object(blob_api, "get_all_by_workspace")
    @patch.object(workspace_api, "can_user_read_workspace")
    @patch.object(workspace_api, "can_user_write_workspace")
    @patch.object(common_views, "ResultsPaginator")
    @patch.object(common_views, "UserForm")
    @patch.object(user_api, "get_id_username_dict")
    @patch.object(user_api, "get_all_users")
    @patch.object(user_api, "get_user_by_id")
    @patch.object(common_views, "reverse")
    @patch.object(common_views.DashboardWorkspaceTabs, "common_render")
    def test_admin_side_context_has_owner_info(
        self,
        mock_common_render,
        mock_reverse,
        mock_get_user_by_id,
        mock_get_all_users,
        mock_get_id_username_dict,
        mock_user_form,
        mock_results_paginator,
        mock_can_user_write_workspace,
        mock_can_user_read_workspace,
        mock_get_all_blob_by_workspace,
        mock_get_all_data_by_workspace,
        mock_workspace_get_by_id,
    ):
        """test_admin_side_context_has_owner_info"""
        mock_common_render.side_effect = self.mock_render_only_context

        self.workspace_records_view.administration = True
        response = RequestMock.do_request_get(
            self.workspace_records_view.as_view(),
            self.user,
            param={"workspace_id": 42},
        )

        self.assertIn("owner", response.keys())
        self.assertIn("owner_change_url", response.keys())
