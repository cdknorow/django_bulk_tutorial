FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install --no-install-recommends --yes postgresql-client
COPY ./requirements.txt .
RUN pip install -r requirements.txt