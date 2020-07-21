# django-libreoffice-converter
An example Django service that converts files into multiple workers using LibreOffice.

## Requirements

* Docker 2.0.0.2 or more
* Docker-compose 1.23.2 or more

## Stack

* Python 3.7
* Django 2.2.13
* Django REST Framework 3.11.0
* Gunicorn 20.0.4
* LibreOffice 6.1.5.2

## Run server

To start the `django-libreoffice-converter`, use the following command in the project folder:
```
docker-compose up
```
App should be up on http://localhost:8000, running Gunicorn in development mode.

## Test
To run tests you can use the follow command inside container (in folder project):
```
pytest
```

## Code style
To reformat all code in the project (except `web/settings`) run the follow command:
```
black web --exclude web/settings -l 100
```

To check whether the code can be reformatted run the follow command:
```
black web --check --exclude web/settings -l 100
```
