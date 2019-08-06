"""Registration and Login class views."""

from flask import jsonify, request
from flask.views import MethodView

from api.auth.auth_utils import generate_user_token
from api.users.models import Users


class Register(MethodView):
    """ View to handle user registration"""
    def post(self):
        data = request.get_json()

        # Assign request body entities
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")

        try:
            user = Users(
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.set_password(password)

            # save user to database
            user.save(user)
            data = {
                "status": "Success",
                "message": "New user created successfully.",
                "details": "{}".format(user)
            }
            return jsonify(data), 201

        except AssertionError as error:
            error_data = {
                    "status": "Failure",
                    "error": "{}".format(error)
                }
            return jsonify(error_data), 400


class Login(MethodView):
    """ View to handle user login"""
    def post(self):

        data = request.get_json()

        try:
            user_token = generate_user_token(data)

            data = {
                "status": "Success",
                "message": "Authentication token succesfully assigned",
                "token": user_token.decode("UTF-8"),
            }
            return jsonify(data)

        except AssertionError as error:
            error_data = {
                    "status": "Failure",
                    "error": "{}".format(error)
                }
            return jsonify(error_data), 401
