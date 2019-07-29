"""Booking model module"""

from api.common.models import BaseModel, db
from api.common.utils import generate_id


class Booking(BaseModel):
    """Booking Model."""
    __tablename__ = "booking"
    id = db.Column(
        db.String(80),
        nullable=False,
        primary_key=True,
        default=generate_id
    )
    flight_id = db.Column(db.String(50), db.ForeignKey('flight.id'))
    flight = db.relationship('Flight')
    customer = db.Column(db.String(50), db.ForeignKey('users.id'))
    user = db.relationship('Users')
    seats_to_book = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Return a string representation for the model."""
        return "Booking: {} on {}".format(self.customer, self.flight_id)
