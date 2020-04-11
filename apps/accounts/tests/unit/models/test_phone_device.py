# -*- coding: utf-8 -*-

import pytest

from apps.accounts.tests.factories.device import PhoneDeviceFactory


@pytest.mark.django_db
class PhoneDeviceTests:

    @staticmethod
    def test_string_representation():
        phone_device = PhoneDeviceFactory()
        str_output = '{token} - {user}'.format(
            token=phone_device.token,
            user=phone_device.user,
        )
        assert str(phone_device) == str_output
