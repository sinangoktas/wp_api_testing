# Can not connect to db (Local's in-build mysql) from docker
# Therefore dockerizing this app for now is on hold
FROM python:latest

MAINTAINER sinang@somemail.com

RUN apt-get update && apt-get -y install vim

RUN mkdir /wp_api_testing

COPY ./automation_code /wp_api_testing/automation_code
COPY ./requirements.txt /wp_api_testing

WORKDIR /wp_api_testing

RUN pip install -r requirements.txt