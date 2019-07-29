# Flight-Booking-Application

[![Build Status](https://travis-ci.org/owenbob/Flight-Booking-Application.svg?branch=master)](https://travis-ci.org/owenbob/Flight-Booking-Application) [![Coverage Status](https://coveralls.io/repos/github/owenbob/Flight-Booking-Application/badge.svg?branch=master)](https://coveralls.io/github/owenbob/Flight-Booking-Application?branch=master) [![CircleCI](https://circleci.com/gh/owenbob/Flight-Booking-Application.svg?style=svg)](https://circleci.com/gh/owenbob/Flight-Booking-Application)

---

## Product overview 
Flight-Booking-Application is a simple REST application built to enable a user to register, login  and book available flights. The available flights are created by the admin user of the application. After a booking has been made, the platform  sends you a confirmatory email and a timely reminder of your flight a day before the flight. The system enables you to also update  your profile picture as to whatever image you might so wish. 

## Development set up
- Check that python 3, pip, virtualenv and postgres are installed

- Clone  Flight-Booking-Application  repo and cd into it
    ```
    https://github.com/owenbob/Flight-Booking-Application.git
    ```
- Create virtual env
    ```
    virtualenv --python=python3 venv
    ```
- Activate virtual env
    ```
    source venv/bin/activate
    ```
- Install dependencies
    ```
    pip install -r requirements.txt
    ```
- Create Application environment variables and save them in .env file.
- Check .env_example for more clarity and enviroment variables to export.
- Run command
    ```
    source .env
    ```
- Running migrations

     ```
     python manage.py db init
    ```
     ```
     python manage.py db migrate
    ```
     ```
     python manage.py db upgrade
    ```
- Run application.
    ```
    python run.py
    ```

## Built with 
- Python version  3
- Flask
- Postgres
- Celery
- Redis
- Google Cloud Storage