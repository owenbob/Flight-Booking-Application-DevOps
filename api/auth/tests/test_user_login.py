"""Test User Login ."""

from api.auth.tests.mixin import AuthAbstractClass


class UserLoginTestCase(AuthAbstractClass):
    """Class to test user login."""

    def test_user_login_is_succesful(self):
        """Test that a user gets a token on login."""

        # register user
        AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                self.user_data
            )

        # make request
        resp = AuthAbstractClass.make_registration_request(
            self,
            self.login_url,
            self.user_login_data
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIn("token", resp.json)
        self.assertEqual(resp.json.get("status"), "Success")
        self.assertEqual(
            resp.json.get("message"),
            "Authentication token succesfully assigned"
        )

    def test_user_login_fails(self):
        """Test that user login fails when invalid data is used."""

        with self.subTest("With no email or password provided."):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_login_data
            )
            invalid_user_data.pop("email")
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.login_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 401)
            self.assertEqual(
                resp.json.get("error"),
                "Please provide email and password."
            )

        with self.subTest("With a non-existent user information."):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_login_data
            )
            invalid_user_data["email"] = "test_user@gmail.com"
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.login_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 401)
            self.assertEqual(
                resp.json.get("error"),
                "Details provided do not match any registered user."
            )

        with self.subTest("With an invalid password."):
            # register user
            AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                self.user_data
            )

            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_login_data
            )
            invalid_user_data["password"] = "Qwerty12345"
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.login_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 401)
            self.assertEqual(
                resp.json.get("error"),
                "Please provide the right password"
            )
