FROM python:3.10.0-alpine

WORKDIR /usr/stat_inc

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/stat_inc/requirements.txt


RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/stat_inc/requirements.txt \
    && rm -rf /root/.cache/pip


COPY . /usr/stat_inc