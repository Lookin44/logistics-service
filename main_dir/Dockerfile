FROM python:3.11.3-alpine

LABEL maintainer='look-in44@yandex.ru'

WORKDIR /usr/src/main_dir

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
