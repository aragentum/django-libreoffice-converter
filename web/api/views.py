import os
import logging
from uuid import uuid4

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)
from web.api.services.file_storage_service import file_storage_service
from web.api.services.libreoffice_converter_service import libreoffice_converter_service


CONVERTER_CONTENT_TYPES = ['application/msword',
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document']

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def word_to_pdf(request):
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        raise ParseError('Not found file.')

    file_name, file_extension = os.path.splitext(uploaded_file.name)
    if not file_name or not file_extension:
        raise ParseError('Invalid file name.')

    if uploaded_file.content_type not in CONVERTER_CONTENT_TYPES:
        raise ParseError('Invalid file type. Allowed only doc and docx files.')

    uploaded_file_path = os.path.join(settings.CONVERTER_TEMP_FILES_FOLDER, f"{uuid4()}{file_extension}")
    converted_file_path = None
    try:
        file_storage_service.save_file(file_path=uploaded_file_path,
                                       file_source=uploaded_file.read())
        converted_file_path = libreoffice_converter_service.convert_to_pdf(uploaded_file_path)
        converted_file = file_storage_service.read_file(file_path=converted_file_path)

        # remove files
        file_storage_service.remove_file(uploaded_file_path)
        file_storage_service.remove_file(converted_file_path)

        response = HttpResponse(converted_file, 'application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(converted_file_path)}"'
        return response
    except Exception as exception:
        file_storage_service.remove_file(uploaded_file_path)
        if converted_file_path:
            file_storage_service.remove_file(converted_file_path)
        raise exception
