# -*- coding: utf-8 -*-

import json
import base64
import oscrypto.asymmetric
import oscrypto.errors
import requests

from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from apps.contrib.api.exceptions import SimpleValidationError
from apps.contrib.api.parsers import SNSJsonParser
from apps.contrib.response_codes import (
    SNS_ENDPOINT_SUBSCRIBE_FAILED,
    INVALID_SNS_SIGNATURE,
    NOT_SNS_REQUEST,
    METHOD_NOT_ALLOWED,
)


class SNSValidator(object):

    SNS_CERTIFICATE_EXPIRATION = 60 * 60  # 1 hour
    AMZ_SNS_MESSAGE_TYPE = 'HTTP_X_AMZ_SNS_MESSAGE_TYPE'
    AMZ_SNS_MESSAGE_ID = 'HTTP_X_AMZ_SNS_MESSAGE_ID'
    AMZ_SNS_TOPIC_ARN = 'HTTP_X_AMZ_SNS_TOPIC_ARN'

    SNS_HEADERS = [
        AMZ_SNS_MESSAGE_TYPE,
        AMZ_SNS_MESSAGE_ID,
        AMZ_SNS_TOPIC_ARN,
    ]

    SUBSCRIPTION_CONFIRMATION = 'SubscriptionConfirmation'
    NOTIFICATION = 'Notification'
    UNSUBSCRIBE_CONFIRMATION = 'UnsubscribeConfirmation'

    @classmethod
    def get_signing_keys(cls, payload):
        message_type = payload.get('Type')
        common_keys = ['Message', 'MessageId']

        if message_type in ('SubscriptionConfirmation', 'UnsubscribeConfirmation'):
            signing_keys = common_keys + ['SubscribeURL', 'Timestamp', 'Token']
        else:
            if 'Subject' in payload and payload['Subject'] is not None:
                signing_keys = common_keys + ['Subject', 'Timestamp']
            else:
                signing_keys = common_keys + ['Timestamp']
        return signing_keys + ['TopicArn', 'Type']

    @classmethod
    def _get_signature(cls, plain_signature):
        return base64.b64decode(plain_signature)

    @classmethod
    def get_certificate(cls, certificate_url):
        certificate = cache.get(certificate_url)
        if not certificate:
            certificate_response = requests.get(certificate_url)
            certificate = certificate_response.text
            cache.set(certificate_url, certificate, cls.SNS_CERTIFICATE_EXPIRATION)

        return certificate.encode()

    @classmethod
    def _get_content(cls, payload):
        lines = []
        for key in cls.get_signing_keys(payload):
            lines.append(key)
            lines.append(payload[key])
        content = '\n'.join(lines) + '\n'

        return content.encode()

    @classmethod
    def has_valid_signature(cls, payload):

        certificate = cls.get_certificate(payload.get('SigningCertURL'))
        signature = cls._get_signature(payload.get('Signature'))
        content = cls._get_content(payload)

        try:
            oscrypto.asymmetric.rsa_pkcs1v15_verify(
                oscrypto.asymmetric.load_certificate(certificate),
                signature,
                content,
                'sha1',
            )
            return True
        except oscrypto.errors.SignatureError:
            return False

    @classmethod
    def perform_confirm_subscribe(cls, payload):
        subscribe_url = payload.get('SubscribeURL')
        if subscribe_url:
            subscribe_response = requests.get(subscribe_url)
            if not subscribe_response.ok:
                raise SimpleValidationError(**SNS_ENDPOINT_SUBSCRIBE_FAILED)

    @classmethod
    def is_confirmation_required(cls, sns_message_type):
        confirmation_types = [cls.SUBSCRIPTION_CONFIRMATION, cls.UNSUBSCRIBE_CONFIRMATION]
        return sns_message_type in confirmation_types

    @classmethod
    def validate_endpoint_confirmation(cls, sns_message_type, payload):
        if cls.is_confirmation_required(sns_message_type):
            cls.perform_confirm_subscribe(payload)

    @classmethod
    def validate_sns_method(cls, method):
        if method != 'POST':
            raise SimpleValidationError(**METHOD_NOT_ALLOWED)

    @classmethod
    def validate_sns_headers(cls, request_headers):
        if not any(elem in SNSValidator.SNS_HEADERS for elem in request_headers):
            raise SimpleValidationError(**NOT_SNS_REQUEST)

    @classmethod
    def validate_signature(cls, payload):
        if not cls.has_valid_signature(payload):
            raise SimpleValidationError(**INVALID_SNS_SIGNATURE)

    @classmethod
    def process_sns_request(cls, request):
        request_headers = [h for h in request.META.keys()]
        cls.validate_sns_method(request.method)
        cls.validate_sns_headers(request_headers)
        sns_message_type = request.META[cls.AMZ_SNS_MESSAGE_TYPE]
        payload = json.loads(request.body)
        cls.validate_endpoint_confirmation(sns_message_type, payload)
        cls.validate_signature(payload)


class SNSEndpointMixin(APIView):
    """Mixin to process AWS SNS Notifications"""

    parser_classes = [SNSJsonParser]
    authentication_classes = ()
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def dispatch(self, request, *args, **kwargs):
        SNSValidator.process_sns_request(request)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return Response('', status=status.HTTP_204_NO_CONTENT)
