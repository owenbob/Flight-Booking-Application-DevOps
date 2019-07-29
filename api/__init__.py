"""Initialize Flask Application."""

from flask import Flask

from api.configuration.config import ConfigureApplication
from api.celery.celery_config import make_celery

# Instantiate flask application
app = Flask(__name__)

# Set application environment configuration
app.config.from_object(ConfigureApplication.set_config())

# Celery  wrap
celery = make_celery(app)

# Set up application URLs
from api.auth.views import Register, Login # noqa E402
from api.flight.views import FlightView # noqa E402
from api.bookings.views import BookingView, FlightBookingView # noqa E402
from api.users.views import UserProfilePicView, UsersView # noqa E402

# Registration route
app.add_url_rule('/v1/auth/register/', view_func=Register.as_view("register"))

# Login route
app.add_url_rule('/v1/auth/login/', view_func=Login.as_view("login"))

# Flight route
app.add_url_rule('/v1/flight/', view_func=FlightView.as_view("flights"))

# Flight route
app.add_url_rule('/v1/bookings/', view_func=BookingView.as_view("bookings"))
app.add_url_rule('/v1/bookings/<flight_id>/', view_func=FlightBookingView.as_view("booking_flight")) # noqa E501


# Uploading User profile
app.add_url_rule('/v1/user/profile_picture/', view_func=UserProfilePicView.as_view("user_profile_picture")) # noqa E501

# Users route
app.add_url_rule('/v1/users/<flight_id>/', view_func=UsersView.as_view("users"))  # noqa: E501
