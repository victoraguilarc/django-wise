# -*- coding: utf-8 -*-
import pytest
from doubles import allow
from django.conf import settings
from django.urls import reverse
from constance.test import override_config
from rest_framework import status

from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.accounts.tests.factories.user import generate_user_profile
from apps.accounts.api.account_responses import AccountsResponses
from apps.accounts.services.user_service import UserService
from apps.contrib.utils.testing.unit_tests import mail_outbox, has_same_code, assert_validation_code
from apps.accounts.serializers.session_serializer import SessionSerializer


@pytest.mark.django_db
class RegisterViewTests:

    register_url = reverse('api-accounts:v1:register')

    @override_config(REGISTER_REQUIRES_EMAIL_CONFIRMATION=False)
    def test_register(self, api_client, test_user):
        allow(UserService).register_new_user.and_return(test_user)

        user_data = generate_user_profile()
        response = api_client.post(self.register_url, user_data)
        response_json = response.json()
        serialized_data = SessionSerializer(test_user).data
        assert response.status_code == status.HTTP_200_OK
        assert response_json.keys() == serialized_data.keys()

    @override_config(REGISTER_REQUIRES_EMAIL_CONFIRMATION=True)
    def test_register_with_email_confirmation(self, api_client, test_user):
        allow(UserService).register_new_user.and_return(test_user)

        user_data = generate_user_profile()
        response = api_client.post(self.register_url, user_data)
        response_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert mail_outbox() == 1
        assert response_json.get('code') == AccountsResponses.CONFIRMATION_EMAIL_SENT.get('code')

    def test_register__invalid_email(self, api_client):
        user_data = generate_user_profile()
        user_data['email'] = 'invalid_email'
        response = api_client.post(self.register_url, user_data)
        response_json = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response_json['validation']
        assert len(response_json['validation']['email']) > 0
        assert response_json['validation']['email'][0]['code'] == 'invalid'

    def test_register__existent_email(self, api_client, test_user):
        user_data = generate_user_profile()
        user_data['email'] = test_user.email

        response = api_client.post(self.register_url, user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_validation_code(
            response_json=response.json(),
            attribute='email',
            code=AccountsErrorCodes.EMAIL_ALREDY_USED.code,
        )

    def test_register__forbidden_username(self, api_client):
        forbidden_usernames = settings.USERNAME_BLACKLIST
        user_data = generate_user_profile()
        user_data['username'] = forbidden_usernames[0]

        response = api_client.post(self.register_url, user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_validation_code(
            response_json=response.json(),
            attribute='username',
            code=AccountsErrorCodes.USERNAME_ALREDY_USED.code,
        )

    def test_register__existent_user(self, api_client, test_user):
        user_data = generate_user_profile()
        user_data['username'] = test_user.username
        response = api_client.post(self.register_url, user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_validation_code(
            response_json=response.json(),
            attribute='username',
            code=AccountsErrorCodes.USERNAME_ALREDY_USED.code,
        )
