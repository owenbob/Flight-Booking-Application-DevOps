"""Flight and FlightSeats models module."""
import re

from sqlalchemy.orm import validates

from api.common.models import BaseModel, db
from api.common.utils import validate_entity, generate_id


class Flight(BaseModel):
    """Flight Model."""

    __tablename__ = "flight"
    id = db.Column(
        db.String(80),
        nullable=False,
        primary_key=True,
        default=generate_id
    )
    departure_time = db.Column(db.DateTime, nullable=False)
    departure_from = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    seats = db.relationship(
        'Seats',
        backref='flight',
        uselist=False,
        lazy=True,
        passive_deletes=True
    )

    def __repr__(self):
        """Return a string representation for the model."""
        return "Flight : {} {}".format(self.departure_time, self.departure_from) # noqa E501

    @validates("departure_time")
    def validate_departure_time(self, key, departure_time):
        if not departure_time:
            raise AssertionError("No departure time provided.")

        pattern = r'[\d\d\d\d-][\d\d-][\d\d\s][\d\d:\d\d]'
        if not re.match(pattern, departure_time):
            raise AssertionError("Please provide departure time in the following formats 1999-08-28 00:00, 1999/08/28 00:00") # noqa E501
        return departure_time

    @validates("departure_from")
    def validate_departure_from(self, key, departure_from):
        dept_from = validate_entity(departure_from, "Departure From")
        return dept_from

    @validates("destination")
    def validate_destiation(self, key, destination):
        destination = validate_entity(destination, "Destination")
        return destination


# Context-Sensitive default function
def available_seats_default(context):
    return context.get_current_parameters()['number_of_seats']


class Seats(BaseModel):
    """Seats model."""
    __tablename__ = "seats"
    id = db.Column(
        db.String(80),
        nullable=False,
        primary_key=True,
        default=generate_id
    )
    number_of_seats = db.Column(db.Integer, nullable=False)
    booked_seats = db.Column(db.Integer, nullable=False, default=0)
    available_seats = db.Column(db.Integer, nullable=False, default=available_seats_default)  # noqa E501
    flight_id = db.Column(db.String, db.ForeignKey('flight.id', ondelete="CASCADE"), nullable=False) # noqa E501

    @validates("number_of_seats")
    def validate_destiation(self, key, number_of_seats):
        if not isinstance(number_of_seats, int):
            raise AssertionError("Number of Seats must be specified as an Integer") # noqa E501
        return number_of_seats
