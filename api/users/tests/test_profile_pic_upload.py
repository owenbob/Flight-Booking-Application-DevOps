"""Test case for file Upload."""
from unittest.mock import MagicMock, patch

from api.users.tests.mixin import UserAbstractClass
from api.users.models import Users

MOCK_URL = "https://storage.googleapis.com/flight-app-profile-pictures/Profile_pic_508f99b6-146e-42d1-bc8c-d7b268d919c0"  # noqa: E501


def mock_upload_profile_picture(image):
    return MOCK_URL


class UserProfilePicTestCase(UserAbstractClass):
    @patch(
        "api.users.views.upload_profile_picture",
        MagicMock(return_value=mock_upload_profile_picture(image="test.jpeg")))
    def test_user_upload_is_successful(self):
        resp = self.client.post(
            self.profile_pic_upload_url,
            content_type='multipart/form-data',
            data=self.data,
            headers=self.headers
        )

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json.get("profile_picture_url"), MOCK_URL)

        # check that the profile_pic is saved for the user
        test_user = Users.query.filter(Users.id == self.test_user_one.id).first()  # noqa: E501
        self.assertEqual(test_user.profile_pic, MOCK_URL)

    def test_user_upload_is_unsuccessful(self):
        with self.subTest("With no file provided"):
            resp = self.client.post(
                self.profile_pic_upload_url,
                headers=self.headers
            )
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.json.get("message"), "No file uploaded")

        with self.subTest("With failure from GCP upload"):
            resp = self.client.post(
                self.profile_pic_upload_url,
                content_type='multipart/form-data',
                data=self.data,
                headers=self.headers
            )
            self.assertEqual(resp.status_code, 500)
            self.assertEqual(
                resp.json.get("message"),
                "Failed to upload file to bucket"
            )
