# -*- coding: utf-8 -*-

from django.conf import settings
from twilio.rest import Client


class TwilioClient(object):
    """Twilio API client implementation."""

    @classmethod
    def send_sms(cls, phone_number: str, message: str):
        """Sends and sms to certain phone number with a defined message."""
        client = cls._get_client()

        return client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )

    @classmethod
    def _get_client(cls):
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        return Client(account_sid, auth_token)
