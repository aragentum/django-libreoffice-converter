from django.conf import settings
from rest_framework import serializers

from web.api.consts import (
    TEXT_MIME_TYPES,
    SPREADSHEET_MIME_TYPES,
    PRESENTATION_MIME_TYPES,
    GRAPHIC_MIME_TYPES,
)
from web.api.validators import FileContentTypeValidator


class TextFileSerializer(serializers.Serializer):
    file = serializers.FileField(
        allow_empty_file=False,
        validators=[
            FileContentTypeValidator(
                max_size=settings.CONVERTER_FILE_MAX_SIZE, mime_types=TEXT_MIME_TYPES
            )
        ],
    )

    class Meta:
        fields = ("file",)

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class SpreadsheetFileSerializer(serializers.Serializer):
    file = serializers.FileField(
        allow_empty_file=False,
        validators=[
            FileContentTypeValidator(
                max_size=settings.CONVERTER_FILE_MAX_SIZE, mime_types=SPREADSHEET_MIME_TYPES,
            )
        ],
    )

    class Meta:
        fields = ("file",)

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class PresentationFileSerializer(serializers.Serializer):
    file = serializers.FileField(
        allow_empty_file=False,
        validators=[
            FileContentTypeValidator(
                max_size=settings.CONVERTER_FILE_MAX_SIZE, mime_types=PRESENTATION_MIME_TYPES,
            )
        ],
    )

    class Meta:
        fields = ("file",)

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class GraphicFileSerializer(serializers.Serializer):
    file = serializers.FileField(
        allow_empty_file=False,
        validators=[
            FileContentTypeValidator(
                max_size=settings.CONVERTER_FILE_MAX_SIZE, mime_types=GRAPHIC_MIME_TYPES
            )
        ],
    )

    class Meta:
        fields = ("file",)

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
