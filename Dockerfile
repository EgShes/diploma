FROM python:3.8

RUN apt update && apt upgrade -y
RUN pip install --upgrade pip

COPY requirements/database.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /src

COPY src/database /src
