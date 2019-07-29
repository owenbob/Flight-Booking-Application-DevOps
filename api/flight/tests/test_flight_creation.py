"""Test Flight creation."""


from api.flight.tests.mixin import FlightAbstractClass


class FlightCreationTestCase(FlightAbstractClass):
    """TestCase for flight creation."""
    def test_flight_creation_is_successfull(self):
        """Test that an admin succefully creates a flight."""
        # grant user admin rights
        self.test_user_one.is_admin = True
        self.test_user_one.save(self.test_user_one)

        resp = self.make_flight_request(
            operation="post",
            url=self.flight_url,
            headers=self.headers,
            content_type="application/json",
            data=self.flight_data
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get("status"), "Success")
        self.assertEqual(
            resp.json.get("message"),
            "New Flight created successfully."
        )

    def test_flight_creation_fails(self):
        """Test that flight creation fails."""
        with self.subTest("With no token provided"):
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                content_type="application/json",
                data=self.flight_data
            )
            self.assertEqual(resp.status_code, 401)
            self.assertEqual(
                resp.json.get("message"),
                "Please provide authentication token."
            )

        with self.subTest("With a user who isnt an admin"):
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.headers,
                content_type="application/json",
                data=self.flight_data
            )
            self.assertEqual(resp.status_code, 403)
            self.assertEqual(
                resp.json.get("message"),
                "You do not have permissions to carry out this operation."
            )

        with self.subTest("With an invalid token"):
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.invalid_headers,
                content_type="application/json",
                data=self.flight_data
            )
            self.assertEqual(resp.status_code, 401)
            self.assertEqual(
                resp.json.get("message"), "Invalid token")

        with self.subTest("With no departure time specified"):
            # grant user admin rights
            self.test_user_one.is_admin = True
            self.test_user_one.save(self.test_user_one)
            # remove departure in flight data
            data = self.generate_flight_data_fixture(self.flight_data)
            data.pop("departure_time")
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.headers,
                content_type="application/json",
                data=data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json.get("error"), "No departure time provided.")

        with self.subTest("With departure time in wrong format"):
            data = self.generate_flight_data_fixture(self.flight_data)
            data["departure_time"] = "30-90-1999999"
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.headers,
                content_type="application/json",
                data=data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json.get("error"),
                "Please provide departure time in the following formats 1999-08-28 00:00, 1999/08/28 00:00") # noqa E501

        with self.subTest("With no departure_from specified"):
            # remove departure in flight data
            data = self.generate_flight_data_fixture(self.flight_data)
            data.pop("departure_from")
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.headers,
                content_type="application/json",
                data=data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json.get("error"), "No Departure From provided")

        with self.subTest("With departure_from as an empty string"):
            data = self.generate_flight_data_fixture(self.flight_data)
            data["departure_from"] = " "
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.headers,
                content_type="application/json",
                data=data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json.get("error"), "Departure From cannot be an empty string") # noqa E501

        with self.subTest("With departure_from provided with special characters"): # noqa E501
            data = self.generate_flight_data_fixture(self.flight_data)
            data["departure_from"] = "$__^%&^ "
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.headers,
                content_type="application/json",
                data=data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json.get("error"), "Departure From cannot contain special characters") # noqa E501

        with self.subTest("With no destination specified"):
            data = self.generate_flight_data_fixture(self.flight_data)
            data.pop("destination")
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.headers,
                content_type="application/json",
                data=data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json.get("error"), "No Destination provided")

        with self.subTest("With destination as an empty string"):
            data = self.generate_flight_data_fixture(self.flight_data)
            data["destination"] = " "
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.headers,
                content_type="application/json",
                data=data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json.get("error"), "Destination cannot be an empty string") # noqa E501

        with self.subTest("With destination provided with special characters"):
            data = self.generate_flight_data_fixture(self.flight_data)
            data["destination"] = "B@rcEl0n@ "
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.headers,
                content_type="application/json",
                data=data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json.get("error"), "Destination cannot contain special characters") # noqa E501

        with self.subTest("With no number_of_seats specified"):
            data = self.generate_flight_data_fixture(self.flight_data)
            data.pop("number_of_seats")
            resp = self.make_flight_request(
                operation="post",
                url=self.flight_url,
                headers=self.headers,
                content_type="application/json",
                data=data
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json.get("error"), "Number of Seats must be specified as an Integer") # noqa E501
