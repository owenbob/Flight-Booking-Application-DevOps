"""Users test mixin."""

from io import BytesIO

from api.flight.tests.mixin import FlightAbstractClass


class UserAbstractClass(FlightAbstractClass):
    def setUp(self):
        super().setUp()
        self.profile_pic_upload_url = "/v1/user/profile_picture/"

        image = (BytesIO(b'test'), 'test.jpeg')
        self.data = {
            "image": image
        }
