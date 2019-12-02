import os
import logging
from uuid import uuid4

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)
from web.api.serializers import WordFileSerializer
from web.api.services.file_storage_service import file_storage_service
from web.api.services.libreoffice_converter_service import libreoffice_converter_service


logger = logging.getLogger(__name__)


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
    uploaded_file = file_serializer.validated_data.get('file')

    file_name, file_extension = os.path.splitext(uploaded_file.name)
    uploaded_file_path = os.path.join(settings.CONVERTER_TEMP_FILES_FOLDER,
                                      f"{uuid4()}{file_extension}")
    converted_file_path = None
    try:
        # save and converting uploaded file
        file_storage_service.save_file(file_path=uploaded_file_path,
                                       file_source=uploaded_file.read())
        converted_file_path = libreoffice_converter_service.convert_to_pdf(uploaded_file_path)

        # read converted file
        converted_file = file_storage_service.read_file(file_path=converted_file_path)

        # remove files
        file_storage_service.remove_file(uploaded_file_path)
        file_storage_service.remove_file(converted_file_path)

        # return converted file
        response = HttpResponse(converted_file, 'application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(converted_file_path)}"'
        return response
    except Exception as exception:
        file_storage_service.remove_file(uploaded_file_path)
        if converted_file_path:
            file_storage_service.remove_file(converted_file_path)
        raise exception
