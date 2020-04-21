# -*- coding: utf-8 -*-

import pytest
from rest_framework.exceptions import NotFound

from apps.accounts.models import PhoneDevice
from apps.accounts.response_codes import DEVICE_NOT_FOUND
from apps.accounts.selectors.device_selector import PhoneDeviceSelector
from apps.accounts.tests.factories.device import PhoneDeviceFactory


@pytest.mark.django_db
class DeviceSelectorTests:

    @staticmethod
    def test_get_by_uuid():
        phone_device = PhoneDeviceFactory()
        selected_phone_device = PhoneDeviceSelector.get_by_uuid(str(phone_device.uuid))

        assert selected_phone_device is not None
        assert isinstance(selected_phone_device, PhoneDevice)
        assert selected_phone_device == phone_device

    @staticmethod
    def test_get_by_uuid_not_found():
        with pytest.raises(NotFound) as exec_info:
            PhoneDeviceSelector.get_by_uuid('anything')
        assert exec_info.value.detail.code == DEVICE_NOT_FOUND['code']

