""" Fixtures files for Data Structure
"""
from core_main_app.components.workspace.models import Workspace

from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)
from datetime import date


class DataFixtures(FixtureInterface):
    """Data structure fixtures"""

    data_structure_1 = None
    workspace_1 = None
    data = None
    template = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """

        # NOTE: no xml_content to avoid using unsupported GridFS mock
        self.workspace_1 = Workspace(
            title="Workspace 1", owner="1", read_perm_id="1", write_perm_id="1"
        )
        self.workspace_1.save()

        self.data = Data(
            template=self.template,
            user_id="1",
            dict_content=None,
            title="title",
            workspace=self.workspace_1,
        )
        self.data.last_modification_date = date.today()
        self.data.save()

        self.data_collection = [
            self.workspace_1,
            self.data,
        ]

    def generate_template(self):
        """Generate a Template.

        Returns:

        """
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template.content = xsd
        self.template.hash = ""
        self.template.filename = "filename.xsd"
        self.template.save()
