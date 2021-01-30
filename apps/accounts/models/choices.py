# -*- coding: utf-8 -*-

from apps.contrib.models.enums import BaseEnum

from django.utils.translation import ugettext_lazy as _


class Platform(BaseEnum):
    """Platform options for Phone Devices."""

    ANDROID = 'android'
    IOS = 'ios'
    WEB = 'web'

    @classmethod
    def choices(cls):  # noqa: D102
        return (
            (cls.ANDROID.value, _('Android')),
            (cls.IOS.value, _('iOS')),
            (cls.WEB.value, _('Web')),
        )


class ActionCategory(BaseEnum):
    """Action options for User actions."""

    CONFIRM_EMAIL = 'confirm_email'
    RESET_PASSWORD = 'reset_password'   # noqa: S105
    VERIFY_PHONE_NUMBER = 'verify_phone_number'   # noqa: S105

    @classmethod
    def choices(cls):  # noqa: D102
        return (
            (cls.CONFIRM_EMAIL.value, _('Confirm e-mail')),
            (cls.RESET_PASSWORD.value, _('Reset Password')),
            (cls.VERIFY_PHONE_NUMBER.value, _('Verify Phone Number')),
        )
