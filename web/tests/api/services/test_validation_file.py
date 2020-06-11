import os
import shutil
import tempfile

import magic
import pytest
from os import path, listdir
from django.conf import settings
from rest_framework import serializers

from web.api.consts import TEXT_MIME_TYPES
from web.api.serializers import TextFileSerializer
from web.api.validators import FileContentTypeValidator
from web.tests.consts import IMAGE_FILE, DOCX_FILE, INVALID_IMAGE_FILE, BROKEN_DOCX_FILE, INVALID_DOCX_FILE


@pytest.mark.django_db
def test_file_max_size(client, monkeypatch):
    monkeypatch.setitem(TextFileSerializer._declared_fields, 'file', serializers.FileField(
        allow_empty_file=False,
        validators=[FileContentTypeValidator(max_size=0.1 * 1024 * 1024,  # 0.1Mb
                                             mime_types=TEXT_MIME_TYPES)]))

    with open(DOCX_FILE, 'rb') as docx_file:
        response = client.post('/api/convert/text/to/pdf/', {
            "file": docx_file
        })
        assert response.status_code == 400
        assert response.json() == dict(file=['Ensure this file size is not greater than 102.4'
                                             '\xa0KBs. Your file size is 211.7\xa0KBs.'])


@pytest.mark.django_db
def test_file_min_size(client, monkeypatch):
    monkeypatch.setitem(TextFileSerializer._declared_fields, 'file', serializers.FileField(
        allow_empty_file=False,
        validators=[FileContentTypeValidator(min_size=2 * 1024 * 1024,  # 2Mb
                                             mime_types=TEXT_MIME_TYPES)]))

    with open(DOCX_FILE, 'rb') as docx_file:
        response = client.post('/api/convert/text/to/pdf/', {
            "file": docx_file
        })
        assert response.status_code == 400
        assert response.json() == dict(file=['Ensure this file size is not less than 2.0\xa0MBs. Your file size '
                                             'is 211.7\xa0KBs.'])


@pytest.mark.django_db
def test_broken_file(client):
    with open(BROKEN_DOCX_FILE, 'rb') as image_file:
        response = client.post('/api/convert/text/to/odt/', {
            "file": image_file
        })
    assert response.status_code == 400
    assert response.json() == dict(detail="Unknown conversion error.")


@pytest.mark.django_db
def test_file_type(client):
    with open(INVALID_IMAGE_FILE, 'rb') as image_file:
        response = client.post('/api/convert/text/to/pdf/', {
            "file": image_file
        })
    assert response.status_code == 400
    assert response.json() == dict(file=['Files of type image/pngs are not supported for this converter.'])


@pytest.mark.django_db
def test_invalid_format(client):
    with open(IMAGE_FILE, 'rb') as image_file:
        response = client.post('/api/convert/text/to/pdf/', {
            "file": image_file
        })
        assert response.status_code == 400
        assert response.json() == dict(file=['Files of type image/pngs are not supported for this converter.'])

    with open(INVALID_DOCX_FILE, 'rb') as image_file:
        response = client.post('/api/convert/text/to/pdf/', {
            "file": image_file
        })
        assert response.status_code == 400
        assert response.json() == dict(file=[
            'The incorrect file extension for type '
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document.'
        ])


@pytest.mark.django_db
def test_valid_class_type(client):
    with open(DOCX_FILE, 'rb') as docx_file:
        response = client.post('/api/convert/text/to/pdf/', {
            "file": docx_file
        })
        assert response.status_code == 200

    # create temp directory
    with tempfile.TemporaryDirectory(
            dir=os.path.join(settings.CONVERTER_TEMP_FOLDER)
    ) as temp_dir:

        # unpack response file
        with tempfile.NamedTemporaryFile(
                dir=temp_dir, suffix='.zip'
        ) as temp_file:
            temp_file.write(response.content)
            shutil.unpack_archive(temp_file.name, extract_dir=temp_dir)

        # get all files in tem directory
        files = [f for f in listdir(temp_dir) if path.isfile(path.join(temp_dir, f)) and f != temp_file.name]

        # validate these files
        assert len(files) == 1
        file_path = path.join(temp_dir, files[0])
        with open(file_path, "rb") as converted_file:
            mime_type = magic.from_buffer(converted_file.read(), mime=True)
            assert mime_type == 'application/pdf'
