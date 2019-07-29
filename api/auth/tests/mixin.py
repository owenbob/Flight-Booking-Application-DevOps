"""Test Mixin Module for Auth Abstract class."""

import json

from copy import copy
from api.common.tests.basetest import BaseTestCase


class AuthAbstractClass(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.registration_url = "/v1/auth/register/"
        self.login_url = "/v1/auth/login/"

        self.user_data = {
            "first_name": "Owen",
            "last_name": "Byomuhangi",
            "email": "rolstar@gmail.com",
            "password": "12345Qwerty"
        }

        self.user_login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }

    def generate_user_data_fixture(self, data):
        """Generate various copies of user_data."""
        return copy(data)

    def make_registration_request(self, url, data):
        """Make request for user registration with invalid user data."""
        return self.client.post(
                url,
                content_type='application/json',
                data=json.dumps(data)
            )
