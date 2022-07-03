FROM python:3.10-slim-buster


RUN apt-get update
RUN apt-get install python3-pip -y

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY ./ /app/