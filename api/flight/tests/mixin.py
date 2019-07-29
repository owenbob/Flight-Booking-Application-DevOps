"""Flight Abstract Class Module."""
import json
from copy import copy

from api.common.tests.basetest import BaseTestCase
from api.users.models import Users


class FlightAbstractClass(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_url = "/v1/auth/login/"
        self.flight_url = "/v1/flight/"

        # test user one
        self.test_user_one = Users(
            first_name="Test",
            last_name="User One",
            email="test_user_one@gmail.com",
        )
        self.test_user_one.set_password("Qwerty12345")
        self.test_user_one.save(self.test_user_one)

        # login test_user_one

        login_body_data = {
            "email": "test_user_one@gmail.com",
            "password": "Qwerty12345"
        }
        login_test_user_one = self.client.post(
            self.login_url,
            data=json.dumps(login_body_data),
            content_type="application/json"
            )

        self.token = login_test_user_one.json.get("token")
        self.headers = {
            "Token": self.token
        }
        self.invalid_headers = {
            "Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo"
        }
        self.flight_data = {
            "departure_time": "1999-08-28 00:00",
            "departure_from": "Entebbe International Airport Uganda",
            "destination": "Newark Airport New York",
            "number_of_seats": 71
        }

    def generate_flight_data_fixture(self, data):
        """Generate various copies of flight_data."""
        return copy(data)

    def make_flight_request(self, operation, url, content_type, headers=None, data=None): # noqa E501
        """Make flight request."""
        request = "self.client.{}('{}', content_type='{}',headers={}, data=json.dumps({}))".format(operation, url, content_type, headers, data) # noqa E501
        return eval(request)

    # NOTE: The use of eval should not be encouraged especially when running
    # shell scripts and servers because it introduces a level of complexity
    # for code readability and a security risk is input is being required
    # from the shell from user. It can however be used for testing and small
    # cases but should never be used for code that is meant to be tested.
