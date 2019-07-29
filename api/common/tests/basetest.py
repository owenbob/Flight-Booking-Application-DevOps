""" BaseTest module to test suite set up ."""
from unittest import TestCase

from api import app
from api.common.models import db


class BaseTestCase(TestCase):
    """Test suite abstract class."""

    def setUp(self):
        """Set up test client"""
        # NOTE: In order to successfully set up the test case and make sure
        # that the correct test configurations the environment variable
        # APP_ENVIRONMENT must be set to `testing`.

        self.client = app.test_client()

        # create tables in test database
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        """Remove all test suite utilities."""

        # Remove all tables from test db
        db.session.remove()
        db.drop_all()
