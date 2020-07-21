from rest_framework import status
from rest_framework.exceptions import APIException


class LibreOfficeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "LibreOffice error."
    default_code = "error"
