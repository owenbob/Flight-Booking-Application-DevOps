"""utility functions for books."""


def list_flights(flights):
    """List view for flights."""
    return [view_flight(flight) for flight in flights]


def view_flight(flight):
    """Return a dict obj of a flight."""
    return {
        "id": flight.id,
        "departure_time": flight.departure_time,
        "departure_from": flight.departure_from,
        "destination": flight.destination,
        "created_at": flight.created_at,
        "updated_at": flight.updated_at,
        "seats": seats(flight)
    }


def seats(flight):
    """Return dict obj of a seat."""
    if flight.seats is None:
        return {}
    else:
        return {
            "id": flight.seats.id,
            "number_of_seats": flight.seats.number_of_seats,
            "booked_seats": flight.seats.booked_seats,
            "available_seats": flight.seats.available_seats,
            "created_at": flight.seats.created_at,
            "updated_at": flight.seats.updated_at
        }


def check_available_seats(flight, seats):
    """Check if seats are available."""

    if not isinstance(seats, int):
            raise AssertionError("Seats must be specified as an Integer")
    # check that the seats to be books are available
    if seats > flight.seats.available_seats:
        raise AssertionError("Seats not available. Only {} seats are available.".format(flight.seats.available_seats))  # noqa: E501


def set_available_seats(seats, user_booked_seats):
    """update the available seats."""
    # get booked seats
    booked_seats = seats.booked_seats + user_booked_seats

    # get available_seats
    available_seats = seats.available_seats - user_booked_seats

    # Set new values for available and booked seats
    seats.booked_seats = booked_seats
    seats.available_seats = available_seats
    seats.save(seats)
