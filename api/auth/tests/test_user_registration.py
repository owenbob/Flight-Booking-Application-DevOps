"""Test User Registration."""

from api.auth.tests.mixin import AuthAbstractClass


class UserRegistrationTestCase(AuthAbstractClass):
    """Class to test user registration."""

    def test_user_registers_sucessfully(self):
        """Test that a user is created succesfully."""
        resp = AuthAbstractClass.make_registration_request(
            self,
            self.registration_url,
            self.user_data
        )
        self.assertEqual(resp.status_code, 201)
        self.assertIn(self.user_data["first_name"], resp.json.get("details"))
        self.assertIn(self.user_data["last_name"], resp.json.get("details"))

    def test_user_registration_fails(self):
        """Test that user registration fails when invalid data is provided."""

        with self.subTest("With no password provided"):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data.pop("password")
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn("No password provided", resp.json.get("error"))

        with self.subTest("With password that contains no capital letter or number"): # noqa E501
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data["password"] = "qwertyasdfgzxcvb"
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                "Password must contain atleast a capital letter and a number",
                resp.json.get("error")
            )

        with self.subTest("With password length not between 10 or 30 characters"): # noqa E501
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data["password"] = "Qwerty123"
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                "Password must be between 10 and 30 characters",
                resp.json.get("error")
            )

        with self.subTest("With no email provided"):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data.pop("email")
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn("No email provided", resp.json.get("error"))

        with self.subTest("With email already used"):

            # register user
            AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                self.user_data
            )

            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                "rolstar@gmail.com is already in use.Provide another email.",
                resp.json.get("error")
            )

        with self.subTest("With an invalid email"):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data["email"] = "qwertyasdfgzxcvb.com"
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                "qwertyasdfgzxcvb.com is an invalid email",
                resp.json.get("error")
            )
        with self.subTest("With no first name provided"):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data.pop("first_name")
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn("No First Name provided", resp.json.get("error"))

        with self.subTest("With an empty string provided for first name"):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data["first_name"] = " "
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                "First Name cannot be an empty string",
                resp.json.get("error")
            )

        with self.subTest("With first name containing special characters"):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data["first_name"] = "S@den!"
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                "First Name cannot contain special characters",
                resp.json.get("error")
            )

        with self.subTest("With no last name provided"):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data.pop("last_name")
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn("No Last Name provided", resp.json.get("error"))

        with self.subTest("With an empty string provided for last name"):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data["last_name"] = " "
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                "Last Name cannot be an empty string",
                resp.json.get("error")
            )

        with self.subTest("With last name containing special characters"):
            invalid_user_data = AuthAbstractClass.generate_user_data_fixture(
                self,
                self.user_data
            )
            invalid_user_data["last_name"] = "R!ch@rl!$on"
            resp = AuthAbstractClass.make_registration_request(
                self,
                self.registration_url,
                invalid_user_data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                "Last Name cannot contain special characters",
                resp.json.get("error")
            )
