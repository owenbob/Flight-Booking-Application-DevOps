"""."""

from api.bookings.tests.mixin import BookingAbstractClass


class ViewFlightsTestCase(BookingAbstractClass):
    """Testcase for viewing flights."""

    def test_flight_listing(self):
        """Test that flights can be listed."""
        resp = self.make_flight_request(
            operation="get",
            url=self.list_flights_url,
            content_type="application/json",
            headers=self.headers
        )

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(isinstance(resp.json, list))
        self.assertEqual(len(resp.json), 1)

    def test_retrieve_a_flight(self):
        """test that a flight can be retrieved."""
        url = "/v1/bookings/{}/".format(self.test_flight.id)
        resp = self.make_flight_request(
            operation="get",
            url=url,
            content_type="application/json",
            headers=self.headers
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get("destination"), self.test_flight.destination)  # noqa: E501

    def test_flight_retrieval_is_unsuccessful(self):
        """Test that retrieval fails with inaccurate flight id."""
        url = "/v1/bookings/159955aa-4bd4-4d7b-b909-ca7173f/"
        resp = self.make_flight_request(
            operation="get",
            url=url,
            content_type="application/json",
            headers=self.headers
        )
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json.get("status"), "Failure")
        self.assertEqual(resp.json.get("message"), "Flight with id 159955aa-4bd4-4d7b-b909-ca7173f Not found")  # noqa: E501
