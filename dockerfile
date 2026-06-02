FROM --platform=linux/arm64 python:3.12.11-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .