import os
import logging
from rest_framework.exceptions import NotFound

from web.api.consts import *
from web.api.serializers import *
from web.api.utils import Service
from web.api.services.libreoffice_converter_service import libreoffice_converter_service


class ConverterUtilService(Service):
    logger = logging.getLogger(__name__)

    def _define_serializer_and_mime_types(self, converter_class: str) -> (serializers.Serializer, dict):
        Serializer = None
        mime_types = None

        self.logger.debug("Defining serializer and mime types for class '%s'", converter_class)
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
            self.logger.info("Not found mime class `%s`", converter_class)
            raise NotFound('Not found mime class.')
        return Serializer, mime_types

    def _define_mime_to(self, mime_types: dict, extension_to: str) -> str:
        mime_to = None
        for mime, extensions in mime_types.items():
            if extension_to in extensions:
                mime_to = mime
        return mime_to

    def validate_file(self, converter_class, extension_to, request):
        # define serializer, mime_types and mime_to
        Serializer, mime_types = self._define_serializer_and_mime_types(converter_class)
        mime_to = self._define_mime_to(mime_types, extension_to)

        # validate file
        serializer = Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_file = serializer.validated_data.get('file')

        self.logger.debug("File '%s' passed validation", validated_file.name)
        return validated_file, mime_to

    def convert_to(self, file_path, extension_to) -> bytes:
        # convert temporary file using libreoffice
        converted_file_path = libreoffice_converter_service.convert_to(file_path, extension_to)

        # read converted file to memory
        self.logger.debug("Reading temporary converted file '%s'", converted_file_path)
        with open(converted_file_path, "rb") as converted_file:
            raw_converted_file = converted_file.read()

        # remove converted file
        if os.path.isfile(converted_file_path):
            os.remove(converted_file_path)
            self.logger.debug("Temporary converted file '%s' is deleted", converted_file_path)

        return raw_converted_file


converter_util_service = ConverterUtilService()
