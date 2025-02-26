FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --dev --system --deploy

FROM base as dev
COPY . /app
