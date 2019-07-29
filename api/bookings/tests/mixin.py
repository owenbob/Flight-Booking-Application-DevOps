"""Mixin for booking ."""

from api.flight.tests.mixin import FlightAbstractClass
from api.flight.models import Flight, Seats


class BookingAbstractClass(FlightAbstractClass):
    def setUp(self):
        super().setUp()
        self.list_flights_url = "/v1/bookings/"

        self.test_flight = Flight(
            departure_time="2019-09-25 00:00",
            departure_from="Kololo Airstrip Kampala",
            destination="London Heathrow",
        )
        self.test_flight.save(self.test_flight)

        self.test_flight_seats = Seats(
            number_of_seats=59,
            flight_id=self.test_flight.id
        )
        self.test_flight_seats.save(self.test_flight_seats)
        self.booking_creation_body = {"seats_to_book": 3}
        self.create_booking_url = "/v1/bookings/{}/".format(self.test_flight.id)  # noqa: E501
        self.list_booked_users = "/v1/users/{}/".format(self.test_flight.id)
