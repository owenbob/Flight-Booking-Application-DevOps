# Flight-Booking-Application-DevOps

[![Build Status](https://travis-ci.org/owenbob/Flight-Booking-Application.svg?branch=master)](https://travis-ci.org/owenbob/Flight-Booking-Application) [![Coverage Status](https://coveralls.io/repos/github/owenbob/Flight-Booking-Application/badge.svg?branch=master)](https://coveralls.io/github/owenbob/Flight-Booking-Application?branch=master) [![CircleCI](https://circleci.com/gh/owenbob/Flight-Booking-Application.svg?style=svg)](https://circleci.com/gh/owenbob/Flight-Booking-Application)

---

## Product overview 
Flight-Booking-Application is a simple REST application built to enable a user to register, login  and book available flights. The available flights are created by the admin user of the application. After a booking has been made, the platform  sends you a confirmatory email and a timely reminder of your flight a day before the flight. The system enables you to also update  your profile picture as to whatever image you might so wish. 

## Development set up
- Check that docker is installed and running
- Clone  Flight-Booking-Application  repo and cd into it
    ```
    https://github.com/owenbob/Flight-Booking-Application-DevOps.git
    ```
- Run application.
    ```
    docker-compose up
    ```
- Run tests.
    ```
    docker exec -it --env APP_ENVIRONMENT=testing flight_app_backend_core bash -c "nosetests --with-coverage"
    ```
## Built with 
- Python version  3
- Flask
- Postgres
- Celery
- Redis
- Google Cloud Storage
- Docker