
FROM python:3.6.5
RUN mkdir src
WORKDIR src/

ENV APP_ENVIRONMENT "development"
Env SECRET_KEY="*****"
ENV DEV_DATABASE_URI="postgresql://admin:root@database:5432/flight_app"
ENV TEST_DATABASE_URI="postgresql://admin:root@database:5432/flight_app_test"

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

EXPOSE 5000
