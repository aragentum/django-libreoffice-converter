from django.conf import settings
from rest_framework import serializers
from django.core.validators import FileExtensionValidator

from web.api.validators import FileValidator

WORD_CONTENT_TYPES = ('application/msword',
                      'application/vnd.openxmlformats-officedocument.wordprocessingml.document')


class WordFileSerializer(serializers.Serializer):
    file = serializers.FileField(
        allow_empty_file=False,
        validators=[FileValidator(max_size=settings.CONVERTER_FILE_MAX_SIZE,
                                  content_types=WORD_CONTENT_TYPES),
                    FileExtensionValidator(['doc', 'docx'])])

    class Meta:
        fields = ('file',)

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError
