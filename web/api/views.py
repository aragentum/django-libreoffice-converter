import os
import tempfile

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
    file_serializer = WordFileSerializer(data=request.data)
    file_serializer.is_valid(raise_exception=True)
    with tempfile.NamedTemporaryFile() as uploaded_file:
        uploaded_file.write(file_serializer.validated_data.get('file').read())
        converted_file_path = libreoffice_converter_service.convert_to_pdf(uploaded_file.name)
        with open(converted_file_path, "rb") as converted_file:
            raw_converted_file = converted_file.read()
        if os.path.isfile(converted_file_path):
            os.remove(converted_file_path)
        response = HttpResponse(raw_converted_file, 'application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(converted_file_path)}"'
        return response
