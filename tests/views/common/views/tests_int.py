""" Test access to views
"""

from django.test import RequestFactory
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_dashboard_app.views.common.views import DashboardWorkspaceTabs
from tests.views.fixtures import DataFixtures


class TestViewDashboardRecords(IntegrationBaseTestCase):
    """Test View Dashboard Records"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.fixture = DataFixtures()
        self.fixture.insert_data()

    def test_user_can_access_records_if_owner(
        self,
    ):
        """test_user_can_access_records_if_owner

        Returns:
        """

        request = self.factory.get("core_dashboard_workspace_list")
        view = DashboardWorkspaceTabs
        view.administration = False
        request.user = create_mock_user(user_id="1", is_superuser=True)
        response = DashboardWorkspaceTabs.as_view()(
            request, self.fixture.workspace_1.id
        )
        self.assertEqual(response.status_code, 200)
