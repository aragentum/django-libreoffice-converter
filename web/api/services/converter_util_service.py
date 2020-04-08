import os
import logging
import shutil
import uuid

from rest_framework.exceptions import NotFound, ValidationError

from web.api.consts import *
from web.api.serializers import *
from web.api.utils import Service
from web.api.services.libreoffice_converter_service import libreoffice_converter_service


class ConverterUtilService(Service):
    logger = logging.getLogger(__name__)

    def _define_serializer(self, converter_class: str) -> (serializers.Serializer, dict):
        self.logger.debug("Defining serializer and mime types for class '%s'", converter_class)
        if converter_class == ConverterClass.TEXT:
            return TextFileSerializer, TEXT_MIME_TYPES
        elif converter_class == ConverterClass.SPREADSHEET:
            return SpreadsheetFileSerializer, SPREADSHEET_MIME_TYPES
        elif converter_class == ConverterClass.PRESENTATION:
            return PresentationFileSerializer, PRESENTATION_MIME_TYPES
        elif converter_class == ConverterClass.GRAPHIC:
            return GraphicFileSerializer, GRAPHIC_MIME_TYPES
        else:
            self.logger.info("Not found mime class `%s`", converter_class)
            raise NotFound('Not found converter class.')

    def _validate_extension_to(self, extension_to: str, mime_types: dict) -> bool:
        for extensions in mime_types.values():
            if extension_to in extensions:
                return True
        self.logger.info("Invalid extension to '%s'", extension_to)
        raise ValidationError(f"Invalid resulting extension '{extension_to}'.")

    def validate_file(self, converter_class: str, extension_to: str, request):
        # define serializer and mime_types
        Serializer, mime_types = self._define_serializer(converter_class)

        # validate extension to
        self._validate_extension_to(extension_to, mime_types)

        # validate file
        serializer = Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_file = serializer.validated_data.get('file')

        self.logger.debug("File '%s' passed validation for converting to '%s'", validated_file.name, extension_to)
        return validated_file

    def convert_to(self, file_path, output_dir, extension_to, archive=True):
        file_path = libreoffice_converter_service.convert_to(file_path, output_dir, extension_to)
        return self.zip_dir(output_dir) if archive else file_path

    def zip_dir(self, dir_path: str, file_path: str = None) -> str:
        zip_file_name = f'{file_path or uuid.uuid4()}'
        zip_file_path = os.path.join(os.path.abspath(os.path.join(dir_path, '..')), zip_file_name)
        zip_file_path = shutil.make_archive(zip_file_path, 'zip', dir_path)
        self.logger.debug("Created zip archive %s", zip_file_name)
        return zip_file_path


converter_util_service = ConverterUtilService()
