# -*- coding: utf-8 -*-

from django.conf import settings
from twilio.rest import Client


class TwilioClient(object):
    @classmethod
    def _get_client(cls):
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        return Client(account_sid, auth_token)

    @classmethod
    def send_sms(cls, phone_number: str, message: str):
        client = cls._get_client()

        return client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )
