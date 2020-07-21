import os

import magic
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from rest_framework.exceptions import ValidationError


@deconstructible
class FileContentTypeValidator(object):
    error_messages = {
        "max_size": (
            "Ensure this file size is not greater than {max_size}s." " Your file size is {size}s."
        ),
        "min_size": (
            "Ensure this file size is not less than {min_size}s. " "Your file size is {size}s."
        ),
        "mime_type": "Files of type {mime_type}s are not supported for this converter.",
        "extension": "The incorrect file extension for type {mime_type}.",
    }

    def __init__(self, max_size=None, min_size=None, mime_types=dict):
        self.max_size = max_size
        self.min_size = min_size
        self.mime_types = mime_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            raise ValidationError(
                self.error_messages["max_size"].format(
                    max_size=filesizeformat(self.max_size), size=filesizeformat(data.size),
                ),
                "min_size",
            )

        if self.min_size is not None and data.size < self.min_size:
            raise ValidationError(
                self.error_messages["min_size"].format(
                    min_size=filesizeformat(self.min_size), size=filesizeformat(data.size),
                ),
                "min_size",
            )

        if self.mime_types:
            mime_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            # validate mime
            extensions = self.mime_types.get(mime_type, None)
            if extensions is None:
                raise ValidationError(
                    self.error_messages["mime_type"].format(mime_type=mime_type), "mime_type",
                )

            # validate extension
            extension = os.path.splitext(data.name)[-1] if "." in data.name else None
            extension = extension.strip(".").lower() if extension is not None else None
            if extension is None or extension not in extensions:
                raise ValidationError(
                    self.error_messages["extension"].format(mime_type=mime_type), "extension",
                )

    def __eq__(self, other):
        return (
            isinstance(other, FileContentTypeValidator)
            and self.max_size == other.max_size
            and self.min_size == other.min_size
            and self.mime_types == other.mime_types
        )
