
from flask import request, jsonify
from flask.views import MethodView

from api.auth.auth_utils import token_needed, is_admin
from api.bookings.models import Booking

from api.users.utils import (
    list_users,
    upload_profile_picture,
    save_profile_picture
)


class UserProfilePicView(MethodView):
    """Update User file."""
    decorators = [token_needed]

    def post(self, current_user):

        # receive image from user upload
        image = request.files.get("image")
        if not image:
            message = {"message": "No file uploaded"}
            return jsonify(message), 400
        try:

            # upload the image
            url = upload_profile_picture(image)
            save_profile_picture(current_user, url)

            return jsonify({"profile_picture_url": url}), 201

        except Exception:
            error_data = {"message": "Failed to upload file to bucket"}
            return jsonify(error_data), 500


class UsersView(MethodView):
    """ View to handle user functionality."""
    decorators = [is_admin]

    def get(self, current_user, flight_id):
        """List the users who have booked a certain flight."""
        bookings = Booking.query.filter(Booking.flight_id == flight_id).all()
        if bookings == []:
            data = {
                "message": "No bookings for flight {}".format(flight_id),
                "recommendation": "Please ensure that the flight_id is valid"
            }
            return jsonify(data), 200

        users = list_users(bookings)
        data = {
            "result": users,
            "status": "Success"
        }
        return jsonify(data), 200
