import os
import tempfile
import uuid

from urllib.parse import quote

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)
from web.api.serializers import WordFileSerializer
from web.api.services.libreoffice_converter_service import libreoffice_converter_service


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def word_to_pdf(request):
    wf_serializer = WordFileSerializer(data=request.data)
    wf_serializer.is_valid(raise_exception=True)
    validated_file = wf_serializer.validated_data.get('file')

    # create temporary file
    with tempfile.NamedTemporaryFile(dir=settings.CONVERTER_TEMP_FOLDER,
                                     suffix=os.path.splitext(validated_file.name)[-1]) as temp_file:
        temp_file.write(validated_file.read())

        # convert temporary file using libreoffice
        converted_file_path = libreoffice_converter_service.convert_to_pdf(temp_file.name)

        # read converted file to memory
        with open(converted_file_path, "rb") as converted_file:
            raw_converted_file = converted_file.read()

        # remove converted file
        if os.path.isfile(converted_file_path):
            os.remove(converted_file_path)

        # response file
        converted_file_name = str(uuid.uuid4()) + '.pdf'
        response = HttpResponse(raw_converted_file, 'application/pdf')
        response['Content-Disposition'] = f'attachment; filename={quote(converted_file_name)}'
        return response
