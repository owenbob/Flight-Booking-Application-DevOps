"""Module to host sendgrid client."""


import os
import smtplib
import ssl

from datetime import datetime

from api.emails.email_message import flight_booking_confirmation, reminder_email  # noqa: E501
from api.bookings.models import Booking
from api.users.models import Users


def send_mail(user, seats_booked, flight):
    try:
        sender_email = os.getenv("APP_EMAIL")
        context = ssl.create_default_context()
        message = flight_booking_confirmation(user, seats_booked, flight)
        with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), os.getenv("SSL_PORT"), context=context) as server:  # noqa: E501
            server.login(os.getenv("APP_EMAIL"), os.getenv("MAIL_KEY"))
            server.sendmail(
                sender_email, user.email, message.as_string()
            )
            server.close()
    except Exception as e:
        print("...Failed to send email because: {}".format(e))


def send_email_reminder():
    # Determine which users have a flight in the next 24 hours
    # get all bookings whose  flight departure time is less of equal to 1
    now = datetime.utcnow()
    bookings = Booking.query.all()
    # get user and the flight
    reminder_list = [i for i in bookings if (i.flight.departure_time - now).days <= 1 and (i.flight.departure_time - now).days >= 0]  # noqa: E501
    for customer in reminder_list:
        send_reminder(
            user=user_query(customer.customer),
            seats_booked=customer.seats_to_book,
            flight=customer.flight
            )


def send_reminder(user, seats_booked, flight):
    try:
        sender_email = os.getenv("APP_EMAIL")
        context = ssl.create_default_context()
        message = reminder_email(user, seats_booked, flight)
        with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), os.getenv("SSL_PORT"), context=context) as server:  # noqa: E501
            server.login(os.getenv("APP_EMAIL"), os.getenv("MAIL_KEY"))
            server.sendmail(
                sender_email, user.email, message.as_string()
            )
            print(">>>>>>>Email Sent>>>>>>>")
            server.close()
    except Exception as e:
        print("...Failed to send email because: {}".format(e))


def user_query(id):
    """Retun User with provided id."""
    return Users.query.filter(Users.id == id).first()
