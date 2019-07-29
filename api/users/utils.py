
import os
import uuid

from google.cloud import storage
from werkzeug.utils import secure_filename


def upload_profile_picture(image):
    """
    Uploads a file to the bucket.
    Important resources
    - https://pypi.org/project/google-cloud-storage/
    - https://cloud.google.com/storage/docs/
    """
    # name of storage bucket
    bucket_name = os.getenv("BUCKET_NAME")

    # Profile picture storage name
    destination_blob_name = "Profile_pic_{}".format(uuid.uuid4())
    filename = secure_filename(image.filename)

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(filename)
    blob = bucket.blob(destination_blob_name)

    blob.make_public()
    url = blob.public_url
    return url


def save_profile_picture(current_user, url):
    """Save a users profile picture."""
    # save profile_pic
    current_user.profile_pic = url
    current_user.save(current_user)


def list_users(bookings):
    """List view for users."""
    return[view_user(booking.user) for booking in bookings]


def view_user(user):
    """reurn a dict ojb of a user."""
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "profile_pic": user.profile_pic,
    }
