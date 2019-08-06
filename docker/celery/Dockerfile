FROM python:3.6.5

RUN mkdir celery
WORKDIR celery/

ENV BROKER_URL="redis://redis:7777/0"

COPY . .

RUN  pip install --upgrade pip
RUN  pip install celery==4.3.0 redis==3.2.1
