# -*- coding: utf-8 -*-

import pytest
from doubles import allow
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated

from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.contrib.utils.testing.unit_tests import assert_error_code, assert_validation_code
from apps.accounts.services.session_service import SessionService
from apps.accounts.serializers.session_serializer import SessionSerializer


@pytest.mark.django_db
class GoogleLoginTests:
    google_login_url = reverse('api-accounts:v1:google-login')

    def test_missing_token(self, api_client):
        response = api_client.post(self.google_login_url, {})
        assert_validation_code(
            response_json=response.json(),
            attribute='token',
            code='required',
        )

    def test_valid_token(self, api_client, test_user):
        allow(SessionService).process_google_token.and_return(test_user)

        login_data = {'token': 'valid_token'}
        response = api_client.post(self.google_login_url, login_data)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        user_data = SessionSerializer(test_user).data
        assert response_json.keys() == user_data.keys()

    def test_invalid_token(self, api_client):
        allow(SessionService).process_google_token.and_raise(AccountsErrorCodes.INVALID_GOOGLE_TOKEN_ID)

        login_data = {'token': 'valid_token'}
        response = api_client.post(self.google_login_url, login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert_error_code(
            response_json=response.json(),
            code=AccountsErrorCodes.INVALID_GOOGLE_TOKEN_ID.code,
        )

    def test_invalid_issuer(self, api_client):
        allow(SessionService).process_google_token.and_raise(AccountsErrorCodes.INVALID_GOOGLE_TOKEN_ISSUER)

        login_data = {'token': 'invalid_token'}
        response = api_client.post(self.google_login_url, data=login_data)
        response_json = response.json()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert_error_code(
            response_json=response.json(),
            code=AccountsErrorCodes.INVALID_GOOGLE_TOKEN_ISSUER.code,
        )
