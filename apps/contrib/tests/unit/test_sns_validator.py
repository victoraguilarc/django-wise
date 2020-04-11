# -*- coding: utf-8 -*-

import json
import random
import pytest

import oscrypto.asymmetric
import requests_mock
from django.core.cache import cache
from doubles import allow, expect

from rest_framework import status

from apps.contrib.api.exceptions import SimpleValidationError
from apps.contrib.response_codes import (
    NOT_SNS_REQUEST,
    METHOD_NOT_ALLOWED,
    SNS_ENDPOINT_SUBSCRIBE_FAILED,
    INVALID_SNS_SIGNATURE,
)
from apps.contrib.tests.factories.sns import generate_sns_subscription, generate_sns_notification
from apps.contrib.views.sns import SNSValidator, SNSEndpointMixin


class SNSValidatorTests:
    TEST_SUBSCRIBE_URL = 'http://sns.server'
    TEST_SIGNATURE = 'test_signature'
    TEST_SIGNING_CERT_URL = 'https://sns.server/certificate.pem'
    TEST_NOTIFICATION = generate_sns_notification(TEST_SIGNATURE, TEST_SIGNING_CERT_URL)

    @staticmethod
    def test_validate_sns_headers():
        request_headers = [
            SNSValidator.AMZ_SNS_MESSAGE_TYPE,
            SNSValidator.AMZ_SNS_MESSAGE_ID,
            SNSValidator.AMZ_SNS_TOPIC_ARN,
        ]

        result = SNSValidator.validate_sns_headers(request_headers)
        assert result is None

    @staticmethod
    def test_validate_sns_headers_invalid():
        request_headers = []
        with pytest.raises(SimpleValidationError) as exec_info:
            SNSValidator.validate_sns_headers(request_headers)
        assert exec_info.value.detail.code == NOT_SNS_REQUEST['code']

    @staticmethod
    def test_validate_sns_method():
        request_method = 'POST'
        result = SNSValidator.validate_sns_method(request_method)
        assert result is None

    @staticmethod
    def test_validate_sns_method_invalid():
        request_method = random.choice(['GET', 'PUT', 'DELETE'])
        with pytest.raises(SimpleValidationError) as exec_info:
            SNSValidator.validate_sns_method(request_method)
        assert exec_info.value.detail.code == METHOD_NOT_ALLOWED['code']

    def test_validate_endpoint_confirmationq_required(self):
        payload = generate_sns_subscription(subscribe_url=self.TEST_SUBSCRIBE_URL)

        with requests_mock.mock() as mock:
            mock.get(
                self.TEST_SUBSCRIBE_URL,
                text=json.dumps(payload),
                status_code=status.HTTP_200_OK,
            )
            result = SNSValidator.validate_endpoint_confirmation(
                SNSValidator.SUBSCRIPTION_CONFIRMATION,
                payload,
            )

        assert result is None
        assert mock.call_count == 1

    def test_validate_endpoint_confirmation_required_subscription_failed(self):
        payload = generate_sns_subscription(subscribe_url=self.TEST_SUBSCRIBE_URL)

        with requests_mock.mock() as mock:
            mock.get(
                self.TEST_SUBSCRIBE_URL,
                text=json.dumps(payload),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            with pytest.raises(SimpleValidationError) as exec_info:
                SNSValidator.validate_endpoint_confirmation(
                    SNSValidator.SUBSCRIPTION_CONFIRMATION,
                    payload,
                )

        assert exec_info.value.detail.code == SNS_ENDPOINT_SUBSCRIBE_FAILED['code']
        assert mock.call_count == 1

    @staticmethod
    def test_validate_endpoint_confirmation_not_required():
        payload = generate_sns_notification()
        result = SNSValidator.validate_endpoint_confirmation(
            SNSValidator.NOTIFICATION,
            payload,
        )
        assert result is None

    def test_validate_signature_valid(self):
        (allow(oscrypto.asymmetric).rsa_pkcs1v15_verify.and_return(None))
        (allow(oscrypto.asymmetric).load_certificate.and_return('certificate'))

        with requests_mock.mock() as mock:
            mock.get(
                self.TEST_SIGNING_CERT_URL,
                text='test_certificate',
                status_code=status.HTTP_200_OK,
            )

            result = SNSValidator.validate_signature(self.TEST_NOTIFICATION)
        assert result is None

    def test_validate_signature_invalid(self):
        (allow(oscrypto.asymmetric).rsa_pkcs1v15_verify
         .and_raise(oscrypto.errors.SignatureError()))
        (allow(oscrypto.asymmetric).load_certificate.and_return('certificate'))

        with requests_mock.mock() as mock:
            mock.get(
                self.TEST_SIGNING_CERT_URL,
                text='test_certificate',
                status_code=status.HTTP_200_OK,
            )

            with pytest.raises(SimpleValidationError) as exec_info:
                SNSValidator.validate_signature(self.TEST_NOTIFICATION)

        assert exec_info.value.detail.code == INVALID_SNS_SIGNATURE['code']

    def test_get_signing_keys_confirmation(self):
        payload = {'Type': 'SubscriptionConfirmation', 'Subject': '........'}
        keys = SNSValidator.get_signing_keys(payload)
        expected_keys = ['Message', 'MessageId', 'SubscribeURL', 'Timestamp', 'Token', 'TopicArn', 'Type']
        assert keys == expected_keys

    def test_get_signing_keys_notification_subject(self):
        payload = {'Type': 'Notification', 'Subject': '........'}
        keys = SNSValidator.get_signing_keys(payload)
        expected_keys = ['Message', 'MessageId', 'Subject', 'Timestamp', 'TopicArn', 'Type']
        assert keys == expected_keys

    def test_signing_keys_notification(self):
        payload = {'Type': 'Notification'}
        keys = SNSValidator.get_signing_keys(payload)
        expected_keys = ['Message', 'MessageId', 'Timestamp', 'TopicArn', 'Type']
        assert keys == expected_keys

    def test_get_certificate(self):
        cache.clear()
        certtificate_url = 'http://credenttials.server/certificate'
        with requests_mock.mock() as mock:
            mock.get(certtificate_url, text='test_certificate', status_code=status.HTTP_200_OK)
            certificate = SNSValidator.get_certificate(certtificate_url)
        certificate_from_cache = cache.get(certtificate_url)
        assert certificate is not None
        assert certificate_from_cache is not None
        assert certificate.decode() == certificate_from_cache

    def test_process_request(self, rf):
        allow(SNSValidator).validate_endpoint_confirmation.and_return(True)
        allow(SNSValidator).validate_signature.and_return(True)

        headers = {
            'HTTP_X_AMZ_SNS_MESSAGE_TYPE': SNSValidator.NOTIFICATION,
            'HTTP_X_AMZ_SNS_MESSAGE_ID': '......',
            'HTTP_X_AMZ_SNS_TOPIC_ARN': 'xxxxxx',
        }
        payload = '{"Type": "Notification", "Subject": "........"}'
        request = rf.post('/', data=payload, content_type='text/plain', **headers)
        SNSValidator.process_sns_request(request)


class SNSEndpointMixinTests:
    def test_post_dispatch(self, rf):
        allow(SNSValidator).process_sns_request.and_return(True)
        expect(SNSValidator).process_sns_request.once()

        request = rf.post('/', data={}, content_type='text/plain')
        view = SNSEndpointMixin()
        view.setup(request)
        view.dispatch(request)

        response = view.post(request)
        assert response.status_code == status.HTTP_204_NO_CONTENT
