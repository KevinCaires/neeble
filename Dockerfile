FROM python:3.8-alpine3.13

RUN apk add --update bash
RUN apk add --update python3
RUN apk add --update mariadb-dev
RUN apk add --no-cache --virtual .build-deps python3-dev build-base linux-headers gcc
RUN pip3 install --upgrade pip

COPY . .

RUN pip install -r requirements/common.txt
