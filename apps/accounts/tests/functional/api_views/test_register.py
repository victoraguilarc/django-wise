# -*- coding: utf-8 -*-
from constance.test import override_config
from django.conf import settings
from django.urls import reverse

import pytest
from doubles import allow
from rest_framework import status

from apps.accounts import response_codes
from apps.accounts.api.v1.serializers.session import SessionSerializer
from apps.accounts.response_codes import CONFIRMATION_EMAIL_SENT
from apps.accounts.services.user import UserService
from apps.accounts.tests.factories.user import generate_user_profile
from apps.contrib.utils.tests.unit_tests import mail_outbox, has_same_code


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
        assert response_json.get('code') == CONFIRMATION_EMAIL_SENT.get('code')

    def test_register__invalid_email(self, api_client):
        user_data = generate_user_profile()
        user_data['email'] = 'invalid_email'
        response = api_client.post(self.register_url, user_data)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response_json

    def test_register__existent_email(self, api_client, test_user):
        user_data = generate_user_profile()
        user_data['email'] = test_user.email

        response = api_client.post(self.register_url, user_data)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response_json
        assert has_same_code(
            response_codes.EMAIL_ALREDY_USED,
            response_json['email'][0],
        )

    def test_register__forbidden_username(self, api_client):
        forbidden_usernames = settings.USERNAME_BLACKLIST
        user_data = generate_user_profile()
        user_data['username'] = forbidden_usernames[0]

        response = api_client.post(self.register_url, user_data)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response_json
        assert has_same_code(
            response_codes.USERNAME_ALREDY_USED,
            response_json['username'][0],
        )

    def test_register__existent_user(self, api_client, test_user):
        user_data = generate_user_profile()
        user_data['username'] = test_user.username

        response = api_client.post(self.register_url, user_data)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response_json
        assert has_same_code(
            response_codes.USERNAME_ALREDY_USED,
            response_json['username'][0],
        )
