# -*- coding: utf-8 -*-

import pyotp
from typing import Tuple
from constance import config
from django.conf import settings

from apps.accounts.models import User, PendingAction
from apps.contrib.utils.strings import get_lapse
from apps.accounts.models.choices import ActionCategory
from apps.accounts.providers.twilio_client import TwilioClient

from django.utils.translation import ugettext_lazy as _


class OTPService(object):
    """class to process One Time Password flows."""

    @classmethod
    def generate_code(cls):
        totp = pyotp.TOTP(settings.SECRET_KEY)
        return totp.now()  # => 'e.g. 492039'

    @classmethod
    def send_verification_code(cls, phone_number: str, code):
        formatted_message = (
            f'{_("Your code is")}:'
            f'{code}\n@{config.OTP_VALIDATION_URL}  #{code}'
        )
        TwilioClient.send_sms(phone_number, formatted_message)

    @classmethod
    def request_code_verification(cls, user: User, phone_number: str) -> PendingAction:
        creation_date, expiration_date = get_lapse()
        data = {'phone_number': phone_number}
        pending_action = PendingAction.objects.create(
            user=user,
            category=ActionCategory.VERIFY_PHONE_NUMBER,
            creation_date=creation_date,
            expiration_date=expiration_date,
            extra=data,
        )
        cls.send_verification_code(phone_number, cls.generate_code())
        return pending_action
