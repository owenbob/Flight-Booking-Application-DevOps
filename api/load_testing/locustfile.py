import json
import random
from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    def user_login(self):
        self.data = {
                "email": "test_user@gmail.com",
                "password": "QWErty12345"
            }
        self.headers = {'content-type': 'application/json'}
        response = self.client.post(
                "v1/auth/login/",
                data=json.dumps(self.data),
                headers=self.headers,
                name="User login"
                )
        token = response.json().get("token")
        return token

    @task(1)
    def register(self):
        email = "ellenkey{}@gmail.com".format(str(random.randint(1, 100001)))
        self.data = {
                "first_name": "ellen",
                "last_name": "key",
                "email": email,
                "password": "Qwerty12345"
                }
        self.headers = {'content-type': 'application/json'}
        self.client.post(
            "v1/auth/register/",
            data=json.dumps(self.data),
            headers=self.headers,
            name="User registration"
            )

    @task(2)
    def login(self):
        self.user_login()

    @task(3)
    def flight_creation(self):
        self.data = {
                "email": "test_admin@gmail.com",
                "password": "QWErty12345"
            }
        self.headers = {'content-type': 'application/json'}
        response = self.client.post(
                "v1/auth/login/",
                data=json.dumps(self.data),
                headers=self.headers,
                name="User login"
                )
        token = response.json().get("token")

        self.flight_data = {
            "departure_from": "nairobi International Airport kennya",
            "departure_time": "2019-05-30 00:00",
            "destination": "Newark Airport New York",
            "number_of_seats": 10000
        }

        self.headers = {
            'content-type': 'application/json',
            'token': token
            }
        self.client.post(
                "v1/flight/",
                data=json.dumps(self.flight_data),
                headers=self.headers,
                name="Flight Creation"
                )

    @task(3)
    def flight_booking(self):
        token = self.user_login()

        self.booking_data = {
            "seats_to_book": 1
        }
        self.headers = {
            'content-type': 'application/json',
            'token': token
            }
        self.client.post(
                "v1/bookings/0ff4fcb4-6f46-47f7-a346-5b20630075f7/",
                data=json.dumps(self.booking_data),
                headers=self.headers,
                name="Flight Booking"
                )


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
