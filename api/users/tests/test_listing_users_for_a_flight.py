
from api.bookings.tests.mixin import BookingAbstractClass


class ListFlightUsers(BookingAbstractClass):
    """Test Listing all users booked on flight."""

    def test_listing_users_is_successful(self):
        with self.subTest("With correct flight_id"):
            # grant user admin rights
            self.test_user_one.is_admin = True
            self.test_user_one.save(self.test_user_one)

            # make a booking
            self.make_flight_request(
                operation="post",
                url=self.create_booking_url,
                content_type="application/json",
                headers=self.headers,
                data=self.booking_creation_body
            )

            resp = self.make_flight_request(
                operation="get",
                url=self.list_booked_users,
                content_type="application/json",
                headers=self.headers
            )
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json.get("status"), "Success")

        with self.subTest("With flight_id that doesnt have bookings"):
            resp = self.make_flight_request(
                operation="get",
                url="/v1/users/99a0-4d9f-b748-bbceecc21/",
                content_type="application/json",
                headers=self.headers
            )
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json.get("recommendation"), "Please ensure that the flight_id is valid")  # noqa : E501

    def test_listing_users_is_unsuccessful(self):
        # revoke user admin rights
        self.test_user_one.is_admin = False
        self.test_user_one.save(self.test_user_one)

        resp = self.make_flight_request(
            operation="get",
            url=self.list_booked_users,
            content_type="application/json",
            headers=self.headers
        )
        self.assertEqual(resp.status_code, 403)
