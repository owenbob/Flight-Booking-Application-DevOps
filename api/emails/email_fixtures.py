import os


def generate_html_email(user, seats_booked, flight):
    """Generate an email to confirm a flight."""
    BOOKING_CONFIRMATION_EMAIL = """
    <html>
    <body>
    <p>Hello {} {}</p>
    <p>This is to confirm that you have booked {} on flight {} from {} to {} for which the departure time is {}.</p>
    <p>Thank you for using Flight Booking Application.</p>
    <p>For inquiries and any question , kindly use {}</p>
    </body>
    </html>
    """.format(user.first_name, user.last_name, seats_booked, flight.id, flight.destination, flight.departure_from, flight.departure_time, os.getenv("APP_EMAIL"))  # noqa: E501
    return BOOKING_CONFIRMATION_EMAIL


def generate_timely_reminder(user, seats_booked, flight):
    """Generate content for email reminder."""
    EMAIL_REMINDER = """
    <html>
    <body>
    <p>Hello {} {}</p>
    <p>This is to remind that you  booked {} on flight {} from {} to {} for which the departure time is {}.</p>
    <p>Thank you for using Flight Booking Application.</p>
    <p>For inquiries and any question , kindly use {}</p>
    </body>
    </html>
    """.format(user.first_name, user.last_name, seats_booked, flight.id, flight.destination, flight.departure_from, flight.departure_time, os.getenv("APP_EMAIL"))  # noqa: E501
    return EMAIL_REMINDER
