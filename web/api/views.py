from urllib.parse import quote

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from web import __version__
from web.api.services.file_converter_service import file_converter_service


@csrf_exempt
@api_view(["GET"])
def healthcheck(request):
    """
    Returns HTTP 200 OK with version of application.
    """
    return Response({"version": __version__}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def convert(request, converter_class: str, extension_to: str):
    """
    Converts file from request to format which define by converter_class and extension_to.
    """
    converted_file_name, raw_converted_file = file_converter_service.validate_and_convert_file(
        converter_class, extension_to, request
    )

    # response file
    response = HttpResponse(raw_converted_file, "application/zip")
    response["Content-Disposition"] = f"attachment; filename={quote(converted_file_name)}"
    return response
