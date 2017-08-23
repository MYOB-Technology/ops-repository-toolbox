FROM python:3.6.2-alpine3.6

MAINTAINER Song Jin @2017

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

Add . /code
WORKDIR /code
