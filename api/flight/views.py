"""Flight class view."""

from flask import jsonify, request
from flask.views import MethodView

from api.auth.auth_utils import is_admin
from api.flight.models import Flight, Seats


class FlightView(MethodView):
    """ View to handle Flight functionality."""
    decorators = [is_admin]

    def post(self, current_user):
        data = request.get_json()
        dept_time = data.get("departure_time")
        dept_from = data.get("departure_from")
        destination = data.get("destination")
        no_of_seats = data.get("number_of_seats")

        try:
            flight = Flight(
                departure_time=dept_time,
                departure_from=dept_from,
                destination=destination
            )
            flight.save(flight)
            seats = Seats(
                number_of_seats=no_of_seats,
                flight_id=flight.id
            )
            seats.save(seats)
            resp = {
                "status": "Success",
                "message": "New Flight created successfully.",
                "details": "{}".format(flight)
            }
            return jsonify(resp), 200

        except AssertionError as error:
            error_data = {
                    "status": "Failure",
                    "error": "{}".format(error)
                }
            return jsonify(error_data), 400
