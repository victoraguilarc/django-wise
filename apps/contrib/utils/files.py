# -*- coding: utf-8 -*-

import io
from PIL import Image
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import SimpleUploadedFile


def generate_image(height=100, width=100, name='test.png'):
    """Generates a temporal on memory image for testing purposes."""
    temp_image = io.BytesIO()
    image = Image.new('RGBA', size=(height, width), color=(155, 0, 0))
    image.save(temp_image, 'png')
    temp_image.name = name
    temp_image.seek(0)
    return temp_image


def generate_image_file():
    """Generates a temporal on disk image for testing purposes."""
    temporal_file = NamedTemporaryFile(delete=True)
    image_io = generate_image()
    temporal_file.write(image_io.read())
    temporal_file.flush()
    return File(temporal_file)


def load_test_photo():
    """Loads tsting image."""
    with open('web/static/tests/mock.png', 'rb') as image:
        return SimpleUploadedFile(
            name='test.png',
            content=image.read(),
            content_type='image/png',
        )


def clean_static_url(file_url):
    """Generates a temporal on memory image for testing purposes."""
    url = '{hostname}{file_url}'.format(
        hostname=settings.PROJECT_HOSTNAME,
        file_url=file_url,
    )
    return url if settings.DEBUG else file_url
