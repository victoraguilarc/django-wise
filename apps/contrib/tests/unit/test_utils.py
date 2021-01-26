# -*- coding: utf-8 -*-

from io import BytesIO
from datetime import datetime
from django.http import HttpRequest
from django.core.files import File
from django.test.utils import override_settings

from apps.contrib.utils import dates, files
from apps.contrib.models.enums import BaseEnum
from apps.contrib.utils.strings import get_uuid, get_hostname, compute_md5_hash

from django.utils import timezone


class UtilsTests:

    @staticmethod
    def test_generate_image():
        photo = files.generate_image()
        assert photo is not None
        assert isinstance(photo, BytesIO)

    @staticmethod
    def test_generate_image_file():
        photo_file = files.generate_image_file()
        assert photo_file is not None
        assert isinstance(photo_file, File)

    @staticmethod
    def test_now():
        timestamp = dates.now()
        assert isinstance(timestamp, datetime)

    @staticmethod
    def test_ago():
        timestamp = dates.ago(days=1)
        assert isinstance(timestamp, datetime)

    @staticmethod
    def test_after():
        timestamp = dates.after(date=timezone.now(), days=1)
        assert isinstance(timestamp, datetime)

    @staticmethod
    def test_local_datetime():
        timestamp = dates.local_datetime()
        assert isinstance(timestamp, datetime)

    @staticmethod
    def test_get_timeslug():
        str_datetime_slug = dates.get_timeslug()
        assert isinstance(str_datetime_slug, str)

    @staticmethod
    def test_compute_md5_hash():
        test_hash = compute_md5_hash("anything")
        assert isinstance(test_hash, str)

    @staticmethod
    def test_get_uuid():
        test_hash = get_uuid()
        assert isinstance(test_hash, str)

    @staticmethod
    def test_get_uuid_pass_limit():
        test_hash = get_uuid(limit=100)
        assert isinstance(test_hash, str)

    @staticmethod
    def test_get_hostname():
        hostname = get_hostname()
        assert isinstance(hostname, str)

    @staticmethod
    def test_get_hostname_with_request():
        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_HOST'] = 'localhost:8000'

        with override_settings(USE_HTTPS=True):
            hostname = get_hostname(request=request)
            assert isinstance(hostname, str)

        with override_settings(USE_HTTPS=False):
            hostname = get_hostname(request=request)
            assert isinstance(hostname, str)

    @staticmethod
    def test_choices_from_base_enum():
        choices = BaseEnum.choices()
        assert isinstance(choices, list)
