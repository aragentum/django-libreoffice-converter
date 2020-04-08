import os
import logging
import tempfile

from urllib.parse import quote

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)

from web.api.serializers import *
from web.api.services.converter_util_service import converter_util_service


logger = logging.getLogger('web.api.views')


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    logger.debug('Called endpoint /api/sample_api')
    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def convert(request, converter_class: str, extension_to: str):
    extension_to = extension_to.lower()
    validated_file = converter_util_service.validate_file(converter_class, extension_to, request)

    extension_from = (os.path.splitext(validated_file.name)[-1] or "").lower()
    if extension_from == extension_to:
        raise ValidationError('The original extension must not be equal to the resulting extension.')

    logger.debug("Run converting '%s' from %s to .%s", validated_file.name, extension_from, extension_to)

    # create temporary file
    with tempfile.TemporaryDirectory(dir=settings.CONVERTER_TEMP_FOLDER) as temp_dir:
        with tempfile.NamedTemporaryFile(dir=settings.CONVERTER_TEMP_FOLDER, suffix=extension_from) as temp_file:
            temp_file.write(validated_file.read())
            logger.debug('Created temporary file %s', temp_file.name)

            # converting and archive result
            zip_file_path = converter_util_service.convert_to(temp_file.name, temp_dir,
                                                              extension_to, archive=True)

            # reading zip archive
            logger.debug("Reading temporary archive file '%s'", zip_file_path)
            with open(zip_file_path, "rb") as converted_file:
                raw_converted_file = converted_file.read()

            # response file
            converted_file_name = os.path.basename(zip_file_path)
            response = HttpResponse(raw_converted_file, 'application/zip')
            response['Content-Disposition'] = f'attachment; filename={quote(converted_file_name)}'
            logger.debug("File `%s` successful converted", converted_file_name)
            return response
