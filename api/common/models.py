"""Application Parent Model."""

from flask_sqlalchemy import SQLAlchemy

from api import app

from api.common.utils import time_utility, generate_id

# Wrap app in ORM
db = SQLAlchemy(app)


class BaseModel(db.Model):
    """Parent Model for Application."""
    __abstract__ = True
    id = db.Column(
        db.String(80),
        nullable=False,
        primary_key=True,
        default=generate_id
    )
    created_at = db.Column(db.DateTime, nullable=False, default=time_utility)
    updated_at = db.Column(db.DateTime, nullable=False, default=time_utility, onupdate=time_utility)  # noqa: E501

    def save(self, obj):
        """Method to save values to the database."""
        db.session.add(obj)
        db.session.commit()
