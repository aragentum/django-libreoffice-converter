FROM python:3.7
ARG APP_ENV=development

ARG APP_NAME=web
ARG WORKDIR=/usr/src/app
ARG REQUIREMENTS=${APP_NAME}/requirements/${APP_ENV}.txt

WORKDIR ${WORKDIR}

# create the app user
RUN addgroup --system app && adduser --system --ingroup app app

# install dependencies
RUN apt-get update && apt-get install -y python3 python3-pip \
    build-essential libssl-dev libffi-dev python-dev \
    libreoffice

# copy project
COPY ./${APP_NAME} ./${APP_NAME}
COPY ./manage.py ./

COPY ./config/${APP_ENV}/gunicorn.py ./
COPY ./config/${APP_ENV}/entrypoint.sh ./
COPY ./config/${APP_ENV}/logging.conf ./

RUN chmod +x ./entrypoint.sh
RUN pip install -r ${REQUIREMENTS}

# chown all the files to the app user
RUN chown -R app:app $WORKDIR

# change to the app user
USER app

EXPOSE 8000
