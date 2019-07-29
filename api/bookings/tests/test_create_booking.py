"""Module to host Booking creation tests."""

from unittest.mock import patch

from api.bookings.tests.mixin import BookingAbstractClass


class BookingCreationTestCase(BookingAbstractClass):
    """Testcase for booking creation."""

    @patch('api.bookings.views.send_mail')
    def test_booking_is_created_successfully(self, send_mail_mock):
        """test that a flight is booked."""

        resp = self.make_flight_request(
            operation="post",
            url=self.create_booking_url,
            content_type="application/json",
            headers=self.headers,
            data=self.booking_creation_body
        )
        self.assertTrue(send_mail_mock.called)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json.get("status"), "Success")
        self.assertEqual(resp.json.get("message"), "New Booking created successfully.")  # noqa: E501

    def test_booking_creation_fails(self):
        """test flight booking fails."""
        with self.subTest("With wrong flight id"):
            url = "/v1/bookings/296cac-99a0-4d9f-b748-bbceecc21/"

            resp = self.make_flight_request(
                operation="post",
                url=url,
                content_type="application/json",
                headers=self.headers,
                data=self.booking_creation_body
            )
            self.assertEqual(resp.status_code, 404)
            self.assertEqual(resp.json.get("status"), "Failure")
            self.assertEqual(resp.json.get("message"), "Flight with id 296cac-99a0-4d9f-b748-bbceecc21 Not found")  # noqa: E501

        with self.subTest("With fewer vaialble seats that the seats being booked"):  # noqa: E501
            # change number of available seats
            self.test_flight_seats.available_seats = 2
            self.test_flight_seats.save(self.test_flight_seats)

            resp = self.make_flight_request(
                operation="post",
                url=self.create_booking_url,
                content_type="application/json",
                headers=self.headers,
                data=self.booking_creation_body
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.json.get("status"), "Failure")
            self.assertEqual(resp.json.get("error"), "Seats not available. Only 2 seats are available.")  # noqa: E501

        with self.subTest("With the seats_to_books not specified as an Integer"):  # noqa: E501
            request_body = {"seats_to_book": "3"}

            resp = self.make_flight_request(
                operation="post",
                url=self.create_booking_url,
                content_type="application/json",
                headers=self.headers,
                data=request_body
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.json.get("status"), "Failure")
            self.assertEqual(resp.json.get("error"), "Seats must be specified as an Integer")  # noqa: E501
