# django-libreoffice-converter
An example Django service that converts files into multiple workers using LibreOffice.

## Requirements

* Docker 2.0.0.2 or more
* Docker-compose 1.23.2 or more

## Stack

* Python 3.7
* Django 2.2.9
* Django REST Framework 3.10.3
* Gunicorn 20.0.4
* LibreOffice 6.1.5.2

## Run server

To start the `django-libreoffice-converter`, use the following command in the project folder:
```
docker-compose up
```
App should be up on http://localhost:8000, running Gunicorn in development mode.
