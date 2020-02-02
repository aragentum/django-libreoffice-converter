import os
import tempfile
import uuid

from urllib.parse import quote

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)

from web.api.consts import *
from web.api.serializers import *
from web.api.services.libreoffice_converter_service import libreoffice_converter_service


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def convert(request, converter_class: str, extension_from: str, extension_to: str):
    extension_to = extension_to.lower()
    extension_from = extension_from.lower()
    if extension_from == extension_to:
        raise ValidationError('The original extension must not be equal to the resulting extension.')

    # define serializer, mime_types and mime_to
    Serializer, mime_types = _convert_define_serializer_and_mime_types(converter_class)
    mime_to = _convert_define_mime_to(mime_types, extension_to)

    # validate file
    serializer = Serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_file = serializer.validated_data.get('file')

    # create temporary file
    with tempfile.NamedTemporaryFile(dir=settings.CONVERTER_TEMP_FOLDER,
                                     suffix=os.path.splitext(validated_file.name)[-1]) as temp_file:
        temp_file.write(validated_file.read())
        raw_converted_file = _convert_to(temp_file.name, extension_to)
        # response file
        converted_file_name = f'{uuid.uuid4()}.{extension_to}'
        response = HttpResponse(raw_converted_file, mime_to)
        response['Content-Disposition'] = f'attachment; filename={quote(converted_file_name)}'
        return response


def _convert_define_serializer_and_mime_types(converter_class: str) -> (serializers.Serializer, dict):
    Serializer = None
    mime_types = None
    if converter_class == ConverterClass.TEXT:
        Serializer = TextFileSerializer
        mime_types = TEXT_MIME_TYPES
    elif converter_class == ConverterClass.SPREADSHEET:
        Serializer = SpreadsheetFileSerializer
        mime_types = SPREADSHEET_MIME_TYPES
    elif converter_class == ConverterClass.PRESENTATION:
        Serializer = PresentationFileSerializer
        mime_types = PRESENTATION_MIME_TYPES
    elif converter_class == ConverterClass.GRAPHIC:
        Serializer = GraphicFileSerializer
        mime_types = GRAPHIC_MIME_TYPES
    else:
        raise NotFound('Not found mime class.')
    return Serializer, mime_types


def _convert_define_mime_to(mime_types: dict, extension_to: str) -> str:
    mime_to = None
    for mime, extensions in mime_types.items():
        if extension_to in extensions:
            mime_to = mime
    return mime_to


def _convert_to(file_path, extension_to) -> bytes:
    # convert temporary file using libreoffice
    converted_file_path = libreoffice_converter_service.convert_to(file_path, extension_to)

    # read converted file to memory
    with open(converted_file_path, "rb") as converted_file:
        raw_converted_file = converted_file.read()

    # remove converted file
    if os.path.isfile(converted_file_path):
        os.remove(converted_file_path)

    return raw_converted_file
