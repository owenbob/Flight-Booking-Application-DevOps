"""Bookings class view."""

from flask import jsonify, request
from flask.views import MethodView

from api.auth.auth_utils import token_needed
from api.bookings.models import Booking
from api.bookings.utils import (
    check_available_seats,
    list_flights,
    set_available_seats,
    view_flight,
)
from api.common.errors import NotFound
from api.emails.mail_helper import send_mail
from api.flight.models import Flight


class BookingView(MethodView):
    """ View to handle Flight functionality."""
    decorators = [token_needed]

    def get(self, current_user):
        query = Flight.query.all()
        data = list_flights(query)
        return jsonify(data), 200


class FlightBookingView(MethodView):
    decorators = [token_needed]

    def get(self, current_user, flight_id):
        flight = Flight.query.filter(Flight.id == flight_id).first()
        if flight:
            data = view_flight(flight)
            return jsonify(data), 200
        return NotFound.response(self, entity="Flight", id=flight_id)  # noqa: E501

    def post(self, current_user, flight_id):
        # Obtain flight
        flight = Flight.query.filter(Flight.id == flight_id).first()

        if not flight:
            return NotFound.response(self, entity="Flight", id=flight_id)  # noqa: E501

        data = request.get_json()
        seats_to_book = data.get("seats_to_book")

        try:
            # check that seats are not more than the available seats
            check_available_seats(flight, seats_to_book)

            # make booking
            booking = Booking(
                flight_id=flight.id,
                flight=flight,
                customer=current_user.id,
                seats_to_book=seats_to_book
            )
            booking.save(booking)

            # decreament number of seats available
            set_available_seats(flight.seats, seats_to_book)

            # Send  booking confirmation
            send_mail(current_user, seats_to_book, flight)

            data = {
                "status": "Success",
                "message": "New Booking created successfully.",
                "details": "{}".format(booking)
            }
            return jsonify(data), 201

        except AssertionError as error:
            error_data = {
                    "status": "Failure",
                    "error": "{}".format(error)
                }
            return jsonify(error_data), 400
