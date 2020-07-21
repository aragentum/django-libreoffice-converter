import logging
import os
import shutil
import tempfile
import uuid
from typing import Tuple

from rest_framework.exceptions import NotFound, ValidationError

from web.api.consts import *
from web.api.serializers import *
from web.api.services.libreoffice_converter_service import libreoffice_converter_service
from web.api.utils import Service


class FileConverterService(Service):
    """
    Implements logic by converting files.
    """

    logger = logging.getLogger(__name__)

    def validate_file(self, converter_class: str, extension_to: str, request):
        """
        Validates file and param extension_to in request.
        """
        extension_to = (extension_to or "").lower()

        # define serializer and mime_types
        Serializer, mime_types = self._define_serializer(converter_class)

        # validate extension to
        self._validate_extension_to(extension_to, mime_types)

        # validate file
        serializer = Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_file = serializer.validated_data.get("file")

        # validate extension_from
        extension_from = (os.path.splitext(validated_file.name)[-1] or "").lower()
        if extension_from == extension_to:
            raise ValidationError(
                "The original extension must not be equal to the resulting extension."
            )

        self.logger.debug(
            "File '%s' passed validation for converting to '%s'", validated_file.name, extension_to,
        )
        return validated_file, extension_from, extension_to

    def convert_file(
        self, validated_file, extension_from: str, extension_to: str
    ) -> Tuple[str, bytes]:
        """
        Converts file to extension_to format.
        """
        self.logger.debug(
            "Run converting '%s' from %s to .%s", validated_file.name, extension_from, extension_to,
        )

        # create temporary file
        with tempfile.TemporaryDirectory(dir=settings.CONVERTER_TEMP_FOLDER) as temp_dir:
            with tempfile.NamedTemporaryFile(
                dir=settings.CONVERTER_TEMP_FOLDER, suffix=extension_from
            ) as temp_file:
                temp_file.write(validated_file.read())
                self.logger.debug("Created temporary file %s", temp_file.name)

                # converting and archive result
                zip_file_path = file_converter_service._run_convert_process(
                    temp_file.name, temp_dir, extension_to, archive=True
                )

                # reading zip archive
                self.logger.debug("Reading temporary archive file '%s'", zip_file_path)
                with open(zip_file_path, "rb") as converted_file:
                    raw_converted_file = converted_file.read()

                converted_file_name: str = os.path.basename(zip_file_path)
                self.logger.debug("File `%s` successful converted", converted_file_name)
                return converted_file_name, raw_converted_file

    def validate_and_convert_file(self, converter_class: str, extension_to: str, request):
        """
        Combines converting and validation processes.
        """
        validated_file, extension_from, extension_to = self.validate_file(converter_class, extension_to, request)
        return self.convert_file(validated_file, extension_from, extension_to)

    def _define_serializer(self, converter_class: str) -> (serializers.Serializer, dict):
        """
        Defines special serializer by converter_class.
        """
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
            raise NotFound("Not found converter class.")

    def _validate_extension_to(self, extension_to: str, mime_types: dict) -> bool:
        """
        Checks that extension_to exists in allowed types.
        """
        for extensions in mime_types.values():
            if extension_to in extensions:
                return True
        self.logger.info("Invalid extension to '%s'", extension_to)
        raise ValidationError(f"Invalid resulting extension '{extension_to}'.")

    def _run_convert_process(self, file_path, output_dir, extension_to, archive=True):
        """
        Runs file convert process.
        """
        file_path = libreoffice_converter_service.convert_to(file_path, output_dir, extension_to)
        return self._pack_dir_to_zip(output_dir) if archive else file_path

    def _pack_dir_to_zip(self, dir_path: str, file_path: str = None) -> str:
        """
        Packs directory to zip archive.
        """
        zip_file_name = f"{file_path or uuid.uuid4()}"
        zip_file_path = os.path.join(os.path.abspath(os.path.join(dir_path, "..")), zip_file_name)
        zip_file_path = shutil.make_archive(zip_file_path, "zip", dir_path)
        self.logger.debug("Created zip archive %s", zip_file_name)
        return zip_file_path


file_converter_service = FileConverterService()
