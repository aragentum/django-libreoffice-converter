ARG APP_NAME=web
ARG WORKDIR=/usr/src/app
ARG REQUIREMENTS=${APP_NAME}/requirements/development.txt

FROM python:3.7
ARG APP_NAME
ARG WORKDIR
ARG REQUIREMENTS

WORKDIR ${WORKDIR}

COPY ./${APP_NAME} ./${APP_NAME}
COPY ./manage.py ./
COPY ./gunicorn.py ./
COPY ./run.sh ./

RUN chmod +x ./run.sh
RUN pip install -r ${REQUIREMENTS}

RUN apt-get update && apt-get install -y python3 python3-pip \
    build-essential libssl-dev libffi-dev python-dev \
    libreoffice

EXPOSE 8000
