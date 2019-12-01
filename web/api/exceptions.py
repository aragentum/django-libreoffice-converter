from rest_framework import status
from rest_framework.exceptions import APIException


class LibreOfficeError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'LibreOffice error.'
    default_code = 'error'
