""" User models module."""
import re

from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from api.common.models import BaseModel, db
from api.common.utils import validate_entity, generate_id


class Users(BaseModel):
    """User Model."""
    __tablename__ = 'users'

    id = db.Column(
        db.String(80),
        nullable=False,
        primary_key=True,
        default=generate_id
    )
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    profile_pic = db.Column(db.String(150), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    flight_booking = db.relationship('Booking')

    @staticmethod
    def check_password(user_password, provided_password):
        """Verify hashed password"""
        return check_password_hash(user_password, provided_password)

    def __repr__(self):
        """Return a string representation for the model."""
        return "User : {} {}".format(self.first_name, self.last_name)

    def set_password(self, password):
        """Hash password for security."""
        if not password:
            raise AssertionError("No password provided")
        if not re.match(r'\d.*[A-Z]|[A-Z].*\d', password):
            raise AssertionError(
                'Password must contain atleast a capital letter and a number'
            )
        if len(password) < 10 or len(password) > 30:
            raise AssertionError(
                'Password must be between 10 and 30 characters'
            )
        self.password_hash = generate_password_hash(password)

    @validates("email")
    def validate_email(self, key, email):
        """Validate email field input."""
        if not email:
            raise AssertionError("No email provided")
        query = Users.query.filter(Users.email == email).first()
        if query:
            raise AssertionError(
                "{} is already in use.Provide another email.".format(email)
            )

        pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        if not re.match(pattern, email):
            raise AssertionError("{} is an invalid email".format(email))
        return email

    @validates("first_name")
    def validate_first_name(self, key, first_name):
        """Validate first name field input."""
        first_name = validate_entity(first_name, "First Name")
        return first_name

    @validates("last_name")
    def validate_last_name(self, key, last_name):
        """Validate first name field input."""
        last_name = validate_entity(last_name, "Last Name")
        return last_name
