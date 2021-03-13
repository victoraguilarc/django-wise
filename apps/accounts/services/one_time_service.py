# -*- coding: utf-8 -*-

import pyotp
from constance import config

from apps.accounts.models import User, PendingAction
from apps.contrib.utils.strings import get_lapse
from apps.accounts.models.choices import ActionCategory
from apps.accounts.providers.twilio_client import TwilioClient

from django.utils.translation import ugettext_lazy as _


class OTPService(object):
    """class to process One Time Password flows."""

    @classmethod
    def generate_secret_key(cls):
        """Generates a secret to use it in OTPs."""
        return pyotp.random_base32()

    @classmethod
    def generate_code(cls, secret_key: str):
        """Generates codes to send through SMS or things like that."""
        totp = pyotp.TOTP(secret_key)
        return totp.now()  # => 'e.g. 492039'

    @classmethod
    def send_verification_code(cls, phone_number: str, code):
        """Formats a OTP SMS texts."""
        default_message = _('Your One Time Code')
        formatted_message = (
            f'{default_message}: '
            f'{code}.\n\n@{config.OTP_VALIDATION_URL}  #{code}'
        )
        TwilioClient.send_sms(phone_number, formatted_message)

    @classmethod
    def request_code_verification(cls, user: User, phone_number: str) -> PendingAction:
        """Process and OTP for a phone verification."""
        creation_date, expiration_date = get_lapse()
        pending_action = PendingAction.objects.create(
            user=user,
            category=ActionCategory.VERIFY_PHONE_NUMBER,
            creation_date=creation_date,
            expiration_date=expiration_date,
        )
        secret_key = cls.generate_secret_key()
        one_time_code = cls.generate_code(secret_key)
        cls.send_verification_code(phone_number, one_time_code)

        pending_action.extra = {
            'phone_number': phone_number,
            'secret_key': phone_number,
        }
        pending_action.save(update_fields=['extra'])

        return pending_action
