FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

COPY . /app

COPY env.sample /app/.env

WORKDIR /app


RUN apt-get update && apt-get install -y \
        gcc \
        default-libmysqlclient-dev \
        && pip install --upgrade pip --no-cache-dir -r requirements.txt 

EXPOSE 5000
