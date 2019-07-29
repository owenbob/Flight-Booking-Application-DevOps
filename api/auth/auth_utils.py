"""Auth utility functions."""

import datetime
import jwt

from flask import jsonify, request
from functools import wraps

from api import app
from api.users.models import Users


def generate_user_token(data):
    """Utility function to generate a token for a user."""

    # Assign request body entities
    email = data.get("email", None)
    password = data.get("password", None)

    # Validate data
    if email is None or password is None:
        raise AssertionError("Please provide email and password.")
    # check if email is for a registered user
    user = Users.query.filter(Users.email == email).first()

    if not user:
        raise AssertionError(
            "Details provided do not match any registered user."
        )

    # check is the provided password matches that of the user
    verified_password = Users.check_password(user.password_hash, password)

    if not verified_password:
        raise AssertionError("Please provide the right password")

    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=50)
            },
        app.config["SECRET_KEY"],
        algorithm='HS256'
    )
    return token


def token_needed(func):
    """Decorator to protect routes."""
    @wraps(func)
    def decorated(*args, **kwargs):
        # check headers for token
        token = request.headers.get("Token", None)
        if not token:
            data = {"message": "Please provide authentication token"}
            return jsonify(data), 401

        # Decode token
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], "HS256")
            current_user = Users.query.filter(Users.id == data["user_id"]).first() # noqa E501

        except Exception:
            data = {"message": "Invalid token"}
            return jsonify(data), 401
        return func(current_user, *args, **kwargs)
    return decorated


# is_admin decorator
def is_admin(func):
    """Decorator to check if the user has admin rights."""
    @wraps(func)
    def decorated(*args, **kwargs):
        # check headers for token
        token = request.headers.get("Token", None)
        if not token:
            data = {"message": "Please provide authentication token."}
            return jsonify(data), 401

        # Decode token
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], "HS256")
            current_user = Users.query.filter(Users.id == data["user_id"]).first() # noqa E501
            if current_user.is_admin is False:
                data = {"message": "You do not have permissions to carry out this operation."} # noqa E501
                return jsonify(data), 403
        except Exception:
            data = {"message": "Invalid token"}
            return jsonify(data), 401
        return func(current_user, *args, **kwargs)
    return decorated
